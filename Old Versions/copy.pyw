import random
from ctypes import HRESULT, POINTER, pointer
from ctypes.wintypes import LPCWSTR, UINT, LPWSTR

import comtypes
from comtypes import IUnknown, GUID, COMMETHOD

from pathlib import Path

# noinspection PyPep8Naming
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
    IMG_LIBRARY_DIR = Path("C:/Users/alexc/Pictures")
    wallpapers = [*map(str, IMG_LIBRARY_DIR.iterdir())]

    desktop_wallpaper = IDesktopWallpaper.CoCreateInstance()
    monitor_count = desktop_wallpaper.GetMonitorDevicePathCount()
    for i in range(monitor_count):
        monitor_id = desktop_wallpaper.GetMonitorDevicePathAt(i)
        wallpaper = random.choice(wallpapers)
        desktop_wallpaper.SetWallpaper(monitor_id, str(wallpaper))


if __name__ == '__main__':
    main()
