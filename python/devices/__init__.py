import platform
from device import Device

if platform.system() == 'Linux':
    from devices_linux import DeviceManager
elif platform.system() == 'Windows':
    from devices_windows import DeviceManager
else:
    raise NotImplementedError(
        "Unknown Operating System: %s" % platform.system()
    )
