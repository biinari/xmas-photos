import platform
from devices.device import Device

if platform.system() == 'Linux':
    from devices.devices_linux import DeviceManager
elif platform.system() == 'Windows':
    from devices.devices_windows import DeviceManager
else:
    raise NotImplementedError(
        "Unknown Operating System: %s" % platform.system()
    )
