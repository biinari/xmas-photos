class IDeviceManager:

    """
    Interface to manage storage devices.

    Should detect devices added / removed and provide their mount point
    """

    def getDevices(self):
        """
        Get list of devices and call device added callback for each.
        """
        raise NotImplementedError("FIXME: Implement method getDevices")

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