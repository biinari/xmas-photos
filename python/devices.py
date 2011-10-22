class IDeviceManager:

    """
    Interface to manage storage devices.

    Should detect devices added / removed and provide their mount point
    """

    def getMountPoint(self, device_id):
        """
        Return the mount point for given device

        String path if mounted or None if not mounted.
        """
        raise NotImplementedError("FIXME: Implement method getMountPoint")

    def setDeviceAddedCallback(self, callback):
        """
        Set a callback for when a new volume is mounted.
        
        callback should follow this specification
        OnDeviceAdded(device_id, properties)
        """
        raise NotImplementedError(
            "FIXME: Implement method setDeviceAddedCallback"
        )

    def setDeviceRemovedCallback(self, callback):
        """
        Set a callback for when a volume is removed.
        
        callback should follow this specification
        OnDeviceRemove(device_id)
        """
        raise NotImplementedError(
            "FIXME: Implement method setDeviceRemvoedCallback"
        )

class Device:
    """ A storage device """
    device_id = None
    mounted = False
    mount_point = None

import platform
if platform.system() == 'Linux':
    from devices_linux import DeviceManager
elif platform.system() == 'Windows':
    from devices_windows import DeviceManager
else:
    raise NotImplementedError(
        "Unknown Operating System: %s" % platform.system()
    )
