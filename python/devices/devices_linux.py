# Communicate with camera
#
# Waits for camera to connect, then move photos from the camera to
# local storage

import dbus
import gobject
from idevicemanager import IDeviceManager
from device import Device

class DeviceManager(IDeviceManager):

    _deviceAddedCallback = None
    _deviceRemovedCallback = None
    _devices = {}

    def __init__(self):
        # Connect to Hal Manager using the System Bus.
        self.bus = dbus.SystemBus()
        self.hal_manager_obj = self.bus.get_object(
            "org.freedesktop.Hal",
            "/org/freedesktop/Hal/Manager")
        self.hal_manager = dbus.Interface(
            self.hal_manager_obj,
            "org.freedesktop.Hal.Manager")
        self.hal_manager.connect_to_signal("DeviceAdded", self._add)
        self.hal_manager.connect_to_signal("DeviceRemoved", self._remove)

    def getDevices(self):
        devices = self.hal_manager.GetAllDevices()
        for udi in devices:
            device_obj = self.bus.get_object("org.freedesktop.Hal", udi)
            device_int = dbus.Interface(device_obj,
                                        "org.freedesktop.Hal.Device")
            if device_int.QueryCapability("volume"):
                self._addVolume(udi, device_int)
                if self._deviceAddedCallback != None:
                    self._deviceAddedCallback(self._devices[udi])

    def _add(self, udi):
        """Filter events to only run for "volume" devices."""
        device_obj = self.bus.get_object("org.freedesktop.Hal", udi)
        device_int = dbus.Interface(device_obj, "org.freedesktop.Hal.Device")
        
        if device_int.QueryCapability("volume"):
            device = self._addVolume(udi, device_int)
            if self._deviceAddedCallback != None:
                return self._deviceAddedCallback(self._devices[udi])

    def _addVolume(self, udi, volume):
        device = Device()
        device.device_id = udi
        device.device_file = volume.GetProperty("block.device")
        device.label = volume.GetProperty("volume.label")
        device.fstype = volume.GetProperty("volume.fstype")
        device.mounted = volume.GetProperty("volume.is_mounted")
        device.mount_point = volume.GetProperty("volume.mount_point")
        try:
            device.size = volume.GetProperty("volume.size")
        except:
            device.size = 0
        self._devices[udi] = device
        return device

    def _remove(self, udi):
        """Device has been removed."""
        if udi in self._devices:
            device = self._devices[udi]
            del self._devices[udi]
            if self._deviceRemovedCallback != None:
                return self._deviceRemovedCallback(device)

    def setDeviceAddedCallback(self, callback):
        self._deviceAddedCallback = callback

    def setDeviceRemovedCallback(self, callback):
        self._deviceRemovedCallback = callback


if __name__ == '__main__':
    from dbus.mainloop.glib import DBusGMainLoop
    DBusGMainLoop(set_as_default=True)
    loop = gobject.MainLoop()
    deviceManager = DeviceManager()
    def deviceAdded(device):
        print("Device Added: %s" % device.device_id)
        if device.mounted:
            print("mount point: %s" % device.mount_point)
        else:
            print("not mounted")
        print("label: %s" % device.label)
        print("fstype: %s" % device.fstype)
        print("size: %s" %device.size)
        print("")
    def deviceRemoved(device):
        print("Device Removed: %s" %device.device_id)
    deviceManager.setDeviceAddedCallback(deviceAdded)
    deviceManager.setDeviceRemovedCallback(deviceRemoved)
    deviceManager.getDevices()
    loop.run()