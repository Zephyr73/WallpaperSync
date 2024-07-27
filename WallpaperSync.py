import os
import shutil
import colorsys
import math
import time
from typing import Tuple, List
from colorthief import ColorThief
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def euclidean_distance(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))


def adjust_saturation_vibrance(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
    r, g, b = [x / 255.0 for x in color]
    h, _, _ = colorsys.rgb_to_hsv(r, g, b)
    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    return int(r * 255), int(g * 255), int(b * 255)


def get_brightness(rgb: Tuple[int, int, int]) -> float:
    return (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255.0


def get_saturation(rgb: Tuple[int, int, int]) -> float:
    return colorsys.rgb_to_hsv(*[x / 255.0 for x in rgb])[1]


def is_near_white(rgb: Tuple[int, int, int], threshold: float = 240.0) -> bool:
    return get_brightness(rgb) > threshold / 255.0


def check_palette(palette: List[Tuple[int, int, int]], tolerance: float = 10.0, threshold: float = 50.0) -> str:
    def is_greyscale() -> bool:
        return all(abs(r - g) <= tolerance and abs(r - b) <= tolerance and abs(g - b) <= tolerance
                   for r, g, b in palette)

    def is_low_contrast() -> bool:
        return any(euclidean_distance(color1, color2) < threshold
                   for i, color1 in enumerate(palette) for color2 in palette[i + 1:])

    if is_greyscale():
        return 'greyscale'
    if is_low_contrast():
        return 'low_contrast'
    return 'normal'


def process_wallpaper(path_to_wallpaper: str) -> Tuple[List[Tuple[int, int, int]], Tuple[int, int, int]]:
    color_thief = ColorThief(path_to_wallpaper)
    palette = color_thief.get_palette(color_count=6)
    filtered_palette = [color for color in palette if not is_near_white(color)]

    palette_type = check_palette(filtered_palette)
    if palette_type == 'greyscale':
        adjusted_rgb1 = (255, 255, 255)  # White
    elif palette_type == 'low_contrast':
        most_saturated_color = max(filtered_palette, key=get_saturation)
        adjusted_rgb1 = adjust_saturation_vibrance(most_saturated_color)
    else:
        sorted_rgb = sorted(filtered_palette, key=lambda x: get_saturation(x) * (1 - get_brightness(x)),
                            reverse=True)
        adjusted_rgb1 = adjust_saturation_vibrance(sorted_rgb[0])

    return filtered_palette, adjusted_rgb1


def fade_color_transition(client: OpenRGBClient, target_color: RGBColor, duration: int = 1, steps: int = 20):
    current_colors = [device.colors[0] for device in client.devices]
    initial_color = current_colors[0]

    for step in range(steps + 1):
        intermediate_color = RGBColor(
            int(initial_color.red + (target_color.red - initial_color.red) * step / steps),
            int(initial_color.green + (target_color.green - initial_color.green) * step / steps),
            int(initial_color.blue + (target_color.blue - initial_color.blue) * step / steps)
        )
        for device in client.devices:
            colors = [intermediate_color] * len(device.colors)
            device.set_colors(colors)
        time.sleep(duration / steps)


def configure_leds(adjusted_rgb1: Tuple[int, int, int]):
    client = OpenRGBClient('localhost', 6742, 'Wal.py')
    client.connect()

    target_color = RGBColor(*adjusted_rgb1)

    print("Starting fade effect...")
    fade_color_transition(client, target_color)
    print("Color transition completed.")

    print("Monitoring wallpaper changes...")
    client.disconnect()


def print_palette(palette: List[Tuple[int, int, int]]):
    """Print the color palette to the terminal."""
    palette_str = ""
    for color in palette:
        r, g, b = color
        # ANSI escape code for background color
        palette_str += f"\033[48;2;{r};{g};{b}m     \033[0m"  # Display block of color

    print("Filtered Palette (excluding near-white colors):")
    print(palette_str)


def print_adjusted_color(color: Tuple[int, int, int]):
    """Print the adjusted color to the terminal."""
    r, g, b = color
    # ANSI escape code for background color
    print("Adjusted Color:")
    print(f"\033[48;2;{r};{g};{b}m     \033[0m")  # Display block of color


class WallpaperHandler(FileSystemEventHandler):
    def __init__(self, original_path: str, local_path: str):
        self.original_path = original_path
        self.local_path = local_path
        self.last_modified_time = None

    def on_modified(self, event):
        if event.src_path == self.original_path:
            time.sleep(1)  # Delay to prevent duplicate events

            try:
                current_modified_time = os.path.getmtime(self.original_path)
                if self.last_modified_time is None or current_modified_time != self.last_modified_time:
                    print("Wallpaper change detected.")
                    shutil.copy2(self.original_path, self.local_path)

                    filtered_palette, adjusted_rgb1 = process_wallpaper(self.local_path)
                    print_palette(filtered_palette)  # Print palette to terminal
                    print_adjusted_color(adjusted_rgb1)  # Print adjusted color to terminal

                    configure_leds(adjusted_rgb1)
                    self.last_modified_time = current_modified_time

            except PermissionError:
                print("Permission denied: Unable to access or copy the wallpaper file.")


def main():
    appdata = os.getenv('APPDATA')
    if not appdata:
        print("APPDATA environment variable is not set.")
        return

    original_path = os.path.join(appdata, 'Microsoft', 'Windows', 'Themes', 'TranscodedWallpaper')
    if not os.path.isfile(original_path):
        print(f"The file does not exist at: {original_path}")
        return

    local_folder = os.getcwd()
    path_to_wallpaper = os.path.join(local_folder, 'TranscodedWallpaper.png')

    print("Monitoring wallpaper changes...")

    event_handler = WallpaperHandler(original_path, path_to_wallpaper)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(original_path), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
