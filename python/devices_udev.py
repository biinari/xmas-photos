#!/usr/bin/env python
import pyudev
from idevicemanager import IDeviceManager
from device import Device

class DeviceManager(IDeviceManager):
    
    _deviceAddedCallback = None
    _deviceRemovedCallback = None
    _devices = {}

    def __init__(self):
        self.context = pyudev.Context()
    
    def getDevices(self):
        devices = context.list_devices(
            subsystem='block',
            ID_TYPE='disk',
            DEV_TYPE='disk'
        )
        for device in devices:
            self._addVolume(device)
            if self._deviceAddedCallback != None:
                self._deviceAddedCallback(device)

    def _addVolume(device):
        self._devices.append(device)

    def setDeviceAddedCallback(self, callback):
        self._deviceAddedCallback = callback

    def setDeviceRemovedCallback(self, callback):
        self._deviceRemovedCallback = callback
