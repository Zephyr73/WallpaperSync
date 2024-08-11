# WallpaperSync: Dynamic LED Color Synchronization

**WallpaperSync** is a Python script that dynamically adjusts the color of connected RGB LED devices based on your desktop wallpaper using [OpenRGB](https://openrgb.org/). The script continuously monitors the system wallpaper for changes and updates the LED colors to match the most prominent color in the wallpaper. This ensures a visually cohesive environment that aligns with your desktop's aesthetics.

[Here is a demo on how it works](https://www.reddit.com/r/pcmasterrace/comments/1edjz55/made_this_script_that_changes_rgb_color_depending/)
## Features

- Real-time Monitoring: Automatically detects changes to the wallpaper and updates LED colors accordingly.
- Easy to configure and use.

## Requirements

To run WallpaperSync, you'll need to install the following Python libraries:

- [colorthief](https://github.com/fengsp/color-thief-py): For extracting color palette
- [openrgb-python](https://github.com/jath03/openrgb-python): For changing RGB colors in hardware
- [watchdog](https://github.com/gorakhargosh/watchdog): For monitoring file system changes.
- `colorsys`, `math`, `time`, `shutil`, and `os`: Standard Python libraries used in the script.

Clone this repository:
```bash
   git clone https://github.com/Zephyr73/WallpaperSync.git
```
# Usage

1. Ensure you have RGB LED devices connected and the OpenRGB server running on localhost port `6742`.
   - You can also configure the `default ip` and `port` if the script doesnt detect OpenRGB SDK using default values. The config will be saved in a `config.json` file
2. Run the script
```sh
run.bat
```
3. The script will create a venv folder which will include all the required libraries from `requirements.txt`. It will then start monitoring for wallpaper changes and updating LED colors.

   - If for some reason, the dependencies are not properly installed, use this `pip` command:
     
     ```bash
     pip install -r requirements.txt
     ```
## Contributing
Feel free to contribute by submitting issues, suggestions, or pull requests.
