import os
import shutil
import colorsys
import math
from typing import Tuple, List
from colorthief import ColorThief
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

# Define utility functions
def euclidean_distance(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))

def adjust_saturation_vibrance(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
    r, g, b = [x / 255.0 for x in color]
    h, _, _ = colorsys.rgb_to_hsv(r, g, b)
    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    return int(r * 255), int(g * 255), int(b * 255)

def get_brightness(rgb: Tuple[int, int, int]) -> float:
    return 0.2126 * rgb[0] / 255.0 + 0.7152 * rgb[1] / 255.0 + 0.0722 * rgb[2] / 255.0

def get_saturation(rgb: Tuple[int, int, int]) -> float:
    return colorsys.rgb_to_hsv(*[x / 255.0 for x in rgb])[1]

def is_near_white(rgb: Tuple[int, int, int], threshold: float = 240.0) -> bool:
    return get_brightness(rgb) > threshold / 255.0

def check_palette(palette: List[Tuple[int, int, int]], tolerance: float = 10.0, threshold: float = 50.0) -> str:
    def is_greyscale():
        return all(abs(r - g) <= tolerance and abs(r - b) <= tolerance and abs(g - b) <= tolerance for r, g, b in palette)

    def is_low_contrast():
        return any(euclidean_distance(color1, color2) < threshold for i, color1 in enumerate(palette) for color2 in palette[i + 1:])

    if is_greyscale():
        return 'greyscale'
    if is_low_contrast():
        return 'low_contrast'
    return 'normal'

def main():
    appdata = os.getenv('APPDATA')
    if not appdata:
        print("APPDATA environment variable is not set.")
        return

    original_path = os.path.join(appdata, 'Microsoft', 'Windows', 'Themes', 'TranscodedWallpaper')
    if not os.path.isfile(original_path):
        print(f"The file does not exist at: {original_path}")
        return

    print(f"Path to TranscodedWallpaper: {original_path}")
    local_folder = os.getcwd()
    path_to_wallpaper = os.path.join(local_folder, 'TranscodedWallpaper.png')
    shutil.copy2(original_path, path_to_wallpaper)

    color_thief = ColorThief(path_to_wallpaper)
    palette = color_thief.get_palette(color_count=6)
    filtered_palette = [color for color in palette if not is_near_white(color)]

    palette_type = check_palette(filtered_palette)
    if palette_type == 'greyscale':
        adjusted_rgb1 = (255, 255, 255)  # White
    elif palette_type == 'low_contrast':
        most_saturated_color = max(filtered_palette, key=get_saturation)
        print("Accent color RGB (before adjustment):", most_saturated_color)  # Print the RGB of the accent color before adjustment
        adjusted_rgb1 = adjust_saturation_vibrance(most_saturated_color)
    else:
        sorted_rgb = sorted(filtered_palette, key=lambda x: get_saturation(x) * (1 - get_brightness(x)), reverse=True)
        print("Accent color RGB (before adjustment):", sorted_rgb[0])  # Print the RGB of the accent color before adjustment
        adjusted_rgb1 = adjust_saturation_vibrance(sorted_rgb[0])

    print("Filtered Palette (excluding near-white colors):", filtered_palette)
    print("Adjusted color:", adjusted_rgb1)

    def configure_leds():
        client = OpenRGBClient('localhost', 6742, 'Wal.py')
        client.connect()
        target_color = RGBColor(*adjusted_rgb1)

        for device in client.devices:
            print(f'Configuring device: {device.name}')
            colors = [target_color] * len(device.colors)
            device.set_colors(colors)

        client.disconnect()

    configure_leds()

if __name__ == "__main__":
    main()
