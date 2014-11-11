#!/usr/bin/env python2
import pyudev
from devices.idevicemanager import IDeviceManager

class DeviceManager(IDeviceManager):

    _device_added_callback = None
    _device_removed_callback = None
    _devices = {}

    def __init__(self):
        self.context = pyudev.Context()

    def get_devices(self):
        devices = self.context.list_devices(
            subsystem='block',
            ID_TYPE='disk',
            DEV_TYPE='disk'
        )
        for device in devices:
            self._add_volume(device)
            if self._device_added_callback != None:
                self._device_added_callback(device)

    def _add_volume(self, device):
        self._devices.append(device)

    def set_device_added_callback(self, callback):
        self._device_added_callback = callback

    def set_device_removed_callback(self, callback):
        self._device_removed_callback = callback
