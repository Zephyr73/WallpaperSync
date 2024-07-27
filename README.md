# WallpaperSync: Dynamic LED Color Synchronization

**WallpaperSync** is a Python script that dynamically adjusts the color of connected RGB LED devices based on your desktop wallpaper using [OpenRGB](https://openrgb.org/). The script continuously monitors the system wallpaper for changes and updates the LED colors to match the most prominent color in the wallpaper. This ensures a visually cohesive environment that aligns with your desktop's aesthetics.

[Here is a demo on how it works](https://www.reddit.com/r/pcmasterrace/comments/1edjz55/made_this_script_that_changes_rgb_color_depending/)
## Features

- **Real-time Monitoring:** Automatically detects changes to the wallpaper and updates LED colors accordingly.
- **Color Extraction:** Uses `ColorThief` to extract a color palette from the wallpaper image.
- **Color Processing:** Adjusts color saturation and vibrance for better LED color representation.
- **Smooth Transitions:** Applies a smooth fade effect to transition LED colors gradually.
- **Customizable Tolerance:** Configures the detection of greyscale and low-contrast palettes.
- **Error Handling:** Includes error handling for file access and permission issues.

## Requirements

To run WallpaperSync, you'll need to install the following Python libraries:

- [colorthief](https://github.com/fengsp/color-thief-py)
- [openrgb-client](https://github.com/jath03/openrgb-python)
- `watchdog`: For monitoring file system changes.
- `colorsys`, `math`, `time`, `shutil`, and `os`: Standard Python libraries used in the script.

You can install these dependencies using `pip`. Here's a command to install all necessary packages:

```sh
pip install colorthief openrgb watchdog
```

Clone this repository:
```bash
   git clone https://github.com/Zephyr73/WallpaperSync.git
```
# Usage

1. Ensure you have RGB LED devices connected and the OpenRGB server running on localhost port `6742`.
2. Run the script
```sh
python WallpaperSync.py
```
3. The script will start monitoring for wallpaper changes and updating LED colors.

## Notes
- Permissions: You may need to run the script with elevated privileges to access the `TranscodedWallpaper` file due to system protection.
- Error Handling: The script provides messages for permission issues and ensures that the wallpaper file is not in use

## Contributing
Feel free to contribute by submitting issues, suggestions, or pull requests.
