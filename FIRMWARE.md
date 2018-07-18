# Firmware Update
The official Gigabyte K85 RGB control software may prompt you to 
perform a firmware update on the keyboard. The device that I was able to
borrow from a friend failed to update the firmware and was subsequently
unusable as the firmware was wiped but no new firmware was installed.

The device is not bricked, however! The bootloader is still in place
(as can be observed by checking the USB descriptors) and thus it is
possible to flash the firmware again.

**Note**: This method worked for me, it may not work for you. 
Proceed with caution and first read the whole document.

1. Connect the keyboard to a USB 2.0 port
2. Navigate to the installation folder of the Gigabyte control software
(Generally `C:\Program Files (x86)\Gigabyte\*\ `).
3. Open a prompt here (either PowerShell or a command prompt) and 
execute `Flasher.exe -h`. This will load the (already downloaded) 
firmware and flash it into your empty device without questions.

Why the `-h` flag? Well, I don't know. Simply executing the program 
without any arguments resulted in an error (in the UI) that no devices
were detected. Then I tried `-h` to hopefully gain some console-based
help messages, but the flashing started immediately with a UI indicator
and completed successfully. The keyboard was fully functional again
after this.
