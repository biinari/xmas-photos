# Windows device detection
# see http://timgolden.me.uk/python/win32_how_do_i/detect-device-insertion.html

import win32api, win32con, win32gui
from ctypes import c_ushort, c_ulong, Structure

#
# Device change events (WM_DEVICECHANGE wParam)
#
DBT_DEVICEARRIVAL = 0x8000
DBT_DEVICEQUERYREMOVE = 0x8001
DBT_DEVICEQUERYREMOVEFAILED = 0x8002
DBT_DEVICEMOVEPENDING = 0x8003
DBT_DEVICEREMOVECOMPLETE = 0x8004
DBT_DEVICETYPESSPECIFIC = 0x8005
DBT_CONFIGCHANGED = 0x0018

#
# type of device in DevBroadcastHdr
#
DBT_DEVTYP_OEM = 0x00000000
DBT_DEVTYP_DEVNODE = 0x00000001
DBT_DEVTYP_VOLUME = 0x00000002
DBT_DEVTYPE_PORT = 0x00000003
DBT_DEVTYPE_NET = 0x00000004

#
# media types in DBT_DEVTYP_VOLUME
#
DBTF_MEDIA = 0x0001
DBTF_NET = 0x0002

WORD = c_ushort
DWORD = c_ulong

class DevBroadcastHdr(Structure):
    _fields_ = [
        ("dbch_size", DWORD),
        ("dbch_devicetype", DWORD),
        ("dbch_reserved", DWORD)
    ]

class DevBroadcastVolume(Structure):
    _fields_ = [
        ("dbcv_size", DWORD),
        ("dbcv_devicetype", DWORD),
        ("dbcv_reserved", DWORD),
        ("dbcv_unitmask", DWORD),
        ("dbcv_flags", WORD)
    ]

def drive_from_mask(mask):
    n_drive = 0
    while 1:
        if mask & (2 ** n_drive):
            return n_drive
        else:
            n_drive += 1

class Notification(object):

    def __init__(self):
        message_map = {
            win32con.WM_DEVICECHANGE: self.on_device_change
        }

        wnd_class = win32gui.WNDCLASS()
        hinst = wnd_class.hInstance = win32api.GetModuleHandle(None)
        wnd_class.lpszClassName = "DeviceChangeDemo"
        wnd_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wnd_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wnd_class.hbrBackground = win32con.COLOR_WINDOW
        wnd_class.lpfnWndProc = message_map
        class_atom = win32gui.RegisterClass(wnd_class)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(
            class_atom,
            "Device Change Demo",
            style,
            0, 0,
            win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
            0, 0,
            hinst, None
        )

    @staticmethod
    def on_device_change(hwnd_, msg_, wparam, lparam):
        #
        # WM_DEVICECHANGE:
        #  wParam - type of change: arrival, removal etc.
        #  lParam - what's changed?
        #        if it's a volume then...
        #  lParam - what's changed more exactly
        #
        dev_broadcast_hdr = DevBroadcastHdr.from_address(lparam)

        if wparam == DBT_DEVICEARRIVAL:
            print "Something's arrived"

            if dev_broadcast_hdr.dbch_devicetype == DBT_DEVTYP_VOLUME:
                print "It's a volume!"

                dev_broadcast_volume = DevBroadcastVolume.from_address(lparam)
                if dev_broadcast_volume.dbcv_flags & DBTF_MEDIA:
                    print "with some media"
                    drive_letter = drive_from_mask(dev_broadcast_volume.dbcv_unitmask)
                    print "in drive", chr(ord("A") + drive_letter)

        return 1

def main():
    Notification()
    win32gui.PumpMessages()

if __name__ == '__main__':
    main()
