A simple Windows program to change between a list of wallpapers depending on the time of day

SETUP:
1. Add wallpapers to the Wallpapers folder, numbered sequentially (i.e. 100 wallpapers numbered 1 to 100)
    - DO NOT ADD ANY OTHER FILES TO THIS FOLDER
    - 4 wallpapers have been added to demonstrate, made by Matt Vince at https://www.mattvince.com/
2. Edit the config file
    a. If you do not have set sunrise and sunset images and instead want to cycle through all the images over the course of a day, set useSunRiseAndSet to false. Otherwise, set it to true, and set the index values of the desired sunrise and sunset wallpaper and your latitude and longitude.
    b. Set the index of your target monitor and the wallpaper file type.
        - Experimentation may be required to figure out the index of the target monitor, each monitor connected to a PC has an index from 1 to the number of monitors.
4. Create a shortcut of wallpaper-changer.pyw and move it to %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
5. Run the file from the Startup folder or restart your computer

CREDITS:
Original Implementation     -   Urim Bersha     -   https://www.youtube.com/urimberisha
Wallpapers                  -   Matt Vince      -   https://www.mattvince.com/
Sunrise and Sunset API      -   Sunrise Sunset  -   https://sunrise-sunset.org/  