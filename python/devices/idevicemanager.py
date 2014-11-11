class IDeviceManager(object):

    """
    Interface to manage storage devices.

    Should detect devices added / removed and provide their mount point
    """

    def get_devices(self):
        """
        Get list of devices and call device added callback for each.
        """
        raise NotImplementedError("FIXME: Implement method get_devices")

    def set_device_added_callback(self, callback):
        """
        Set a callback for when a new volume is mounted.

        callback should follow this specification
        OnDeviceAdded(device)
        """
        raise NotImplementedError(
            "FIXME: Implement method set_device_added_callback"
        )

    def set_device_removed_callback(self, callback):
        """
        Set a callback for when a volume is removed.

        callback should follow this specification
        OnDeviceRemove(device)
        """
        raise NotImplementedError(
            "FIXME: Implement method setDeviceRemvoedCallback"
        )
