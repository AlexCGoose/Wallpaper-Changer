from ctypes import HRESULT, POINTER, pointer
from ctypes.wintypes import LPCWSTR, UINT, LPWSTR

import comtypes
from comtypes import IUnknown, GUID, COMMETHOD

import json
from pathlib import Path

import time
import datetime

import requests

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
    with open("config.json") as file:
        config = json.load(file)

    wallpaperDir = Path.cwd() / "Wallpapers"
    wallpapers = [*map(str, wallpaperDir.iterdir())]
    wallpaperCount = len(wallpapers)
    
    try:
        lat = float(config["latitude"])
    except ValueError:
        lat = 0.0
    
    try:
        lng = float(config["longitude"])
    except ValueError:
        lng = 0.0

    response = requests.get(f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}").json()
    sunrise = datetime.datetime.strptime(response["results"]["sunrise"], "%I:%M:%S %p")
    sunset = datetime.datetime.strptime(response["results"]["sunset"], "%I:%M:%S %p")

    sunriseMins = sunrise.hour * 60 + sunrise.minute
    sunsetMins = sunset.hour * 60 + sunset.minute

    minsInDay = 24 * 60
    riseToSetMins = sunsetMins - sunriseMins
    setToRiseMins = sunriseMins + minsInDay - sunsetMins
    
    if config["useSunRiseAndSet"]:
        try:
            sunriseIndex = int(config["sunriseIndex"])
            if sunriseIndex < 1 or sunriseIndex > wallpaperCount:
                sunriseIndex = 1
        except ValueError:
            sunriseIndex = 1

        try:
            sunsetIndex = int(config["sunsetIndex"])
            if sunsetIndex < 1 or sunsetIndex > wallpaperCount:
                sunsetIndex = wallpaperCount
        except ValueError:
            sunsetIndex = wallpaperCount
    
    else:
        sunriseIndex = 1
        sunsetIndex = wallpaperCount

    currentTimeMins = (datetime.datetime.now().hour * 60) + datetime.datetime.now().minute

    desktopWallpaper = IDesktopWallpaper.CoCreateInstance()
    monitorId = desktopWallpaper.GetMonitorDevicePathAt(config["targetModitorIndex"])

    if sunriseMins < currentTimeMins < sunsetMins:
        minsPerPic = riseToSetMins / (sunsetIndex - sunriseIndex)
        currentPic = sunriseIndex + (currentTimeMins - sunriseMins) / minsPerPic
    
    elif sunsetMins < currentTimeMins :
        minsPerPic = setToRiseMins / (wallpaperCount - sunsetIndex + sunriseIndex)
        currentPic = int(sunsetIndex + ((currentTimeMins - sunsetMins) / minsPerPic)) % wallpaperCount

    else:
        minsPerPic = setToRiseMins / (wallpaperCount - sunsetIndex + sunriseIndex)
        currentPic = currentTimeMins / minsPerPic

    i = int(currentPic)
    while i <= wallpaperCount:
        fileName = str(i) + '.' + config["wallpaperFileType"]
        path = Path.cwd() / "Wallpapers" / fileName
        desktopWallpaper.SetWallpaper(monitorId, str(path))

        time.sleep(int(60 * minsPerPic))

        i += 1

        if i < sunriseIndex or i > sunsetIndex:
            minsPerPic = setToRiseMins / (wallpaperCount - sunsetIndex + sunriseIndex)
        else:
            minsPerPic = riseToSetMins / (sunsetIndex - sunriseIndex)
        
        if i >= wallpaperCount:
            i = 1

if __name__ == '__main__':
    main()
