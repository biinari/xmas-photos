import platform
from device import Device

class IDeviceManager:

    """
    Interface to manage storage devices.

    Should detect devices added / removed and provide their mount point
    """

    def setDeviceAddedCallback(self, callback):
        """
        Set a callback for when a new volume is mounted.
        
        callback should follow this specification
        OnDeviceAdded(device)
        """
        raise NotImplementedError(
            "FIXME: Implement method setDeviceAddedCallback"
        )

    def setDeviceRemovedCallback(self, callback):
        """
        Set a callback for when a volume is removed.
        
        callback should follow this specification
        OnDeviceRemove(device)
        """
        raise NotImplementedError(
            "FIXME: Implement method setDeviceRemvoedCallback"
        )

if platform.system() == 'Linux':
    from devices_linux import DeviceManager
elif platform.system() == 'Windows':
    from devices_windows import DeviceManager
else:
    raise NotImplementedError(
        "Unknown Operating System: %s" % platform.system()
    )
