# WallpaperSync

**WallpaperSync** is a Python script designed to automatically synchronize your computer's LED lighting with the colors of your desktop wallpaper. By analyzing the color palette of your wallpaper, WallpaperSync adjusts the LED colors to match or complement the wallpaper, enhancing your overall visual experience.

## Features

- **Automatic LED Color Synchronization:** Adjusts LED colors based on your desktop wallpaper.
- **Greyscale Detection:** Sets LEDs to white if the wallpaper is greyscale.
- **Low Contrast & Monochromatic Handling:** Chooses the most saturated color from the palette if the wallpaper is low contrast and monochromatic.
- **Primary Color Matching:** Finds the nearest primary color for accurate LED color representation.
- **Flexible Color Matching:** Uses a pre-defined set of primary colors for LED adjustments.

## Requirements

To run WallpaperSync, you'll need to install the following Python libraries:

- `colorthief`
- `openrgb-client`

You can install these dependencies using `pip`. Here's a command to install all necessary packages:

```sh
pip install colorthief openrgb-client
