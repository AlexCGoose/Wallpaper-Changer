from ctypes import HRESULT, POINTER, pointer
from ctypes.wintypes import LPCWSTR, UINT, LPWSTR

import comtypes
from comtypes import IUnknown, GUID, COMMETHOD

import json
from pathlib import Path

import time
import datetime

import requests

import random

class IDesktopWallpaper(IUnknown):
    # Ref: https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-idesktopwallpaper

    # Search `IDesktopWallpaper` in `\HKEY_CLASSES_ROOT\Interface` to obtain the magic string
    _iid_ = GUID('{B92B56A9-8B55-4E14-9A89-0199BBB6F93B}')

    @classmethod
    def CoCreateInstance(cls):
        # Search `Desktop Wallpaper` in `\HKEY_CLASSES_ROOT\CLSID` to obtain the magic string
        class_id = GUID('{C2CF3110-460E-4fc1-B9D0-8A1C0C9CC4BD}')
        return comtypes.CoCreateInstance(class_id, interface=cls)

    _methods_ = [
        COMMETHOD(
            [], HRESULT, 'SetWallpaper',
            (['in'], LPCWSTR, 'monitorID'),
            (['in'], LPCWSTR, 'wallpaper'),
        ),
        COMMETHOD(
            [], HRESULT, 'GetWallpaper',
            (['in'], LPCWSTR, 'monitorID'),
            (['out'], POINTER(LPWSTR), 'wallpaper'),
        ),
        COMMETHOD(
            [], HRESULT, 'GetMonitorDevicePathAt',
            (['in'], UINT, 'monitorIndex'),
            (['out'], POINTER(LPWSTR), 'monitorID'),
        ),
        COMMETHOD(
            [], HRESULT, 'GetMonitorDevicePathCount',
            (['out'], POINTER(UINT), 'count'),
        ),
    ]

    def SetWallpaper(self, monitorId: str, wallpaper: str):
        self.__com_SetWallpaper(LPCWSTR(monitorId), LPCWSTR(wallpaper))

    def GetWallpaper(self, monitorId: str) -> str:
        wallpaper = LPWSTR()
        self.__com_GetWallpaper(LPCWSTR(monitorId), pointer(wallpaper))
        return wallpaper.value

    def GetMonitorDevicePathAt(self, monitorIndex: int) -> str:
        monitorId = LPWSTR()
        self.__com_GetMonitorDevicePathAt(UINT(monitorIndex), pointer(monitorId))
        return monitorId.value

    def GetMonitorDevicePathCount(self) -> int:
        count = UINT()
        self.__com_GetMonitorDevicePathCount(pointer(count))
        return count.value


def main():
    # Load configuration
    with open("config.json") as file:
        config = json.load(file)

    # Load wallpapers
    wallpaperDir = Path.cwd() / "Wallpapers"
    wallpapers = [*map(str, wallpaperDir.iterdir())]
    wallpaperCount = len(wallpapers)

    # Set wallpaper object and monitor ID
    desktopWallpaper = IDesktopWallpaper.CoCreateInstance()
    monitorId = desktopWallpaper.GetMonitorDevicePathAt(config["targetModitorIndex"])

    if config["randomised"]:
        # Randomise wallpapers every `randomiseInvervalMins` minutes
        while True:
            desktopWallpaper.SetWallpaper(monitorId, random.choice(wallpapers))

            time.sleep(int(60 * config["randomiseInvervalMins"]))
    else:
        # Get latitude and longitude from config
        try:
            lat = float(config["latitude"])
        except ValueError:
            lat = 0.0
        
        try:
            lng = float(config["longitude"])
        except ValueError:
            lng = 0.0

        minsInDay = 24 * 60

        # Checks if sunrise and sunset times are to be used
        if config["useSunRiseAndSet"]:
            # Get sunrise and sunset times from API
            response = requests.get(f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}").json()
            sunrise = datetime.datetime.strptime(response["results"]["sunrise"], "%I:%M:%S %p")
            sunset = datetime.datetime.strptime(response["results"]["sunset"], "%I:%M:%S %p")

            sunriseTimeMins = sunrise.hour * 60 + sunrise.minute
            sunsetTimeMins = sunset.hour * 60 + sunset.minute

            # Set sunrise index
            try:
                sunriseIndex = int(config["sunriseIndex"])
                if sunriseIndex < 1 or sunriseIndex > wallpaperCount:
                    sunriseIndex = 1
            except ValueError:
                sunriseIndex = 1

            # Set sunset index
            try:
                sunsetIndex = int(config["sunsetIndex"])
                if sunsetIndex < 1 or sunsetIndex > wallpaperCount:
                    sunsetIndex = wallpaperCount
            except ValueError:
                sunsetIndex = wallpaperCount
        else:
            # Setting sunrise and sunset times to 0 and 24 hours respectively
            sunriseTimeMins = 0
            sunsetTimeMins = minsInDay

            # Set sunrise and sunset index
            sunriseIndex = 1
            sunsetIndex = wallpaperCount

        # Calculates the time between sunrise and sunset and the time between sunset and sunrise
        riseToSetMins = sunsetTimeMins - sunriseTimeMins
        setToRiseMins = sunriseTimeMins + minsInDay - sunsetTimeMins

        # Gets current time in minutes
        currentTimeMins = (datetime.datetime.now().hour * 60) + datetime.datetime.now().minute

        # Calculates the minutes that should pass between each wallpaper and the current wallpaper index
        if sunriseTimeMins < currentTimeMins < sunsetTimeMins:
            minsPerPic = riseToSetMins / (sunsetIndex - sunriseIndex)
            currentPic = sunriseIndex + (currentTimeMins - sunriseTimeMins) / minsPerPic
        
        elif sunsetTimeMins < currentTimeMins :
            minsPerPic = setToRiseMins / (wallpaperCount - sunsetIndex + sunriseIndex)
            currentPic = int(sunsetIndex + ((currentTimeMins - sunsetTimeMins) / minsPerPic)) % wallpaperCount

        else:
            minsPerPic = setToRiseMins / (wallpaperCount - sunsetIndex + sunriseIndex)
            currentPic = currentTimeMins / minsPerPic

        # Loop through wallpapers
        i = int(currentPic)
        while i <= wallpaperCount:
            # Set wallpaper
            fileName = str(i) + '.' + config["wallpaperFileType"]
            path = Path.cwd() / "Wallpapers" / fileName
            desktopWallpaper.SetWallpaper(monitorId, str(path))

            # Wait for `minsPerPic` minutes
            time.sleep(int(60 * minsPerPic))

            i += 1

            # Recalculate `minsPerPic` if sunrise or sunset is reached
            if i < sunriseIndex or i > sunsetIndex:
                minsPerPic = setToRiseMins / (wallpaperCount - sunsetIndex + sunriseIndex)
            else:
                minsPerPic = riseToSetMins / (sunsetIndex - sunriseIndex)
            
            # Reset index if it exceeds the number of wallpapers
            if i >= wallpaperCount:
                i = 1

if __name__ == '__main__':
    main()
