"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Standard Library
from array import array
# Packages
from usb import core as usb
# Project Modules
from rgbkeyboards.keyboard import BaseKeyboard
from rgbkeyboards.keyboards import register_backend
from rgbkeyboards.utilities import get_platform

iManufacturer = "Texas Instruments"
iProduct = "MSP430-USB Example"
bVendor = 0x1044
bProduct = 0x7a14

WINDOWS = "windows"
LINUX = "linux"


def register(path=None):
    """Register the backend with rgbkeyboards"""
    if path is None and get_platform == WINDOWS:
        raise ValueError("libusb-1.0 DLL path is required for Windows")
    if path is not None and get_platform() == LINUX:
        path = None  # Ignored under Linux
    register_backend(get_platform(), iManufacturer, "gigabyte_k85", path)


PCK_OPTIONS = array('B', [
    # Indices: 6:brightness (0x00-0x05)
    0x3F, 0x08, 0x01, 0xC9, 0x01, 0x05, 0x01, 0x01,
    0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
])

PCK_COLOR = array('B', [
    # Indices: 4:red, 5:green, 6:blue
    0x3F, 0x08, 0x01, 0xC8, 0xFF, 0xFF, 0xFF, 0x01,
    0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
])

InvalidPlatform = RuntimeError("Unsupported platform detected")


class Keyboard(BaseKeyboard):
    """Gigabyte K85 Keyboard backend for rgbkeyboards package"""

    _ENDPOINT = 0x04

    def _setup_lib(self, path=None):
        """Detect the device and set the attribute to it"""
        if path is None and get_platform() == WINDOWS:
            raise ValueError("libusb1 DLL path is required on Windows")
        if path is not None:
            self._setup_pyusb_hook(path)
        self._device = self._get_device_available(True)

    @staticmethod
    def _setup_pyusb_hook(path):
        """Enforce the usage of DLL in pyusb in any function call"""
        from usb import libloader
        __orig_load_locate_library = libloader.load_locate_library

        def hook(*args, **kwargs):
            kwargs.update({"find_library": lambda *args: path})
            return __orig_load_locate_library(*args, **kwargs)

        libloader.load_locate_library = hook

    def _enable_control(self):
        """Enable control on the device by setting default options"""
        if self._device is None:
            raise RuntimeError("No valid device available")
        assert isinstance(self._device, usb.Device)
        if self._device.is_kernel_driver_active(3):
            self._device.detach_kernel_driver(3)
        return self._send_packet(PCK_OPTIONS)

    def _disable_control(self):
        """Close the USB device connection"""
        return True

    def _get_device_available(self, find=False):
        """Find the K85 and return True if it is connected"""
        device = usb.find(idVendor=bVendor, idProduct=bProduct)
        if device is None:
            return False if find is False else None
        if isinstance(device, list):
            device = device[0]
        return True if find is False else device

    def _set_full_color(self, r, g, b):
        """Set the color of all the LEDs on the keyboard"""
        pck = PCK_COLOR.copy()
        pck[4] = r, pck[5] = g, pck[6] = b
        self._send_packet(PCK_OPTIONS)
        return self._send_packet(pck)

    def _set_ind_color(self, keys):
        """Not supported on simpleton single color K85"""
        return True

    def _send_packet(self, packet):
        """Send an array of bytes to the device"""
        assert isinstance(packet, array)
        assert isinstance(self._device, usb.Device)
        w = self._device.write(self._ENDPOINT, packet)
        return w == len(packet)

    @staticmethod
    def is_product_supported(product):
        """Determine whether a product is supported based on iProduct"""
        return product == iProduct
