# K85 RGB Control Interface
Because the K85 only supports a single color for all keys and no 
interesting effect, this is a much shorter interface description than
for the [MasterKeys](https://github.com/RedFantom/masterkeys-linux) 
keyboards.

## USB Interface
```
bVendor: 0x1044 Chu Yuen Enterprise Co., Ltd
bProduct: 0x7a14

iManufacturer: Texas Instruments
iProduct: MSP430-USB Example

Configurations: 1
Interfaces: 4 (!)
```
As you can see in the above code block, the keyboard reports its
manufacturer to be Texas Instruments, and its product to be an
`Example`. This is a great example of lazy manufacturers.

It appears there is only an ANSI variant of this keyboard, and thus
there probably aren't any other `bProduct` ids around.

## Hardware details
The keyboard is indeed powered by a `MSP430` MCU produced by Texas 
Instruments and for which there a great [Reference Design](http://www.ti.com/lit/ug/tidu521/tidu521.pdf),
but it appears that Gigabyte (or the OEM that built this keyboard for
them?) did not move past implementing the RGB functionality and
releasing the software.

Without an actual teardown of the keyboard it is impossible to tell how
the LEDs are really controlled, but my best guess is that the
through-hole mounted RGB LEDs have a common anode and split cathodes
and that all all these LEDs are in parallel. The cathodes of each of 
the colours is then probably connected to the drain of an N-channel
MOSFET that is controlled using PWM from the MCU.

Even if the LEDs were 5050 SMD LEDs or some similar design, the MCU
would probably not be able to control all the LEDs independently and 
provide <1ms response times, in case you were wondering.

## Interfaces and Endpoints
The the USB descriptor reports not one, not two, but four interfaces.
```markdown
# Interface 0: HID Keyboard
Just a plain keyboard interface
EndPoint 1  IN: 0x81, 8 bytes
EndPoint 1 OUT: 0x01, 8 bytes

# Interface 1: HID 64N Interface
Perhaps the firmware updating interface? No idea, really.
EndPoint 1  IN: 0x82, 20 bytes
EndPoint 1 OUT: 0x02: 20 bytes

# Interface 2: HID Mouse (!)
Yeah, this keyboard also has a mouse interface.
EndPoint 3  IN: 0x83, 8 bytes
EndPoint 3 OUT: 0x83, 8 bytes

# Interface 3: HID DataPipeline interface
RGB LED Control interface
EndPoint 4  IN: 0x84, 64 bytes
EndPoint 4 OUT: 0x04, 64 bytes
```

As indicated, only the last interface and endpoints are interesting
here. They provide a really simple interface to controlling the RGB
LEDs.

## RGB Control Protocol
Set the color to `rr, gg, bb` in hex:
```python
3f 08 01 c8 rr gg bb 08 01 00 ..

3f 08 01 09 01 ** 01 01 08 00 ..
```
The ** indicate the brightness parameter. The RGB color can be 
brightness-scaled using the brightness (ranging from `0x00` to `0x05`).
Do yourself a favour and don't use that option anywhere but just adjust
your RGB tuple.

There are two effects available on the K85, probably also sporting
additional parameters set in the second packet, but they are too boring
and can easily be implemented in software. I have not decoded the
protocol for adjusting that.

## Practical implications
Just send the second listed packet once, and then simply adjust the 
color of the LEDs by only sending the first packet with different
RGB color values. The second packet is not needed to adjust the color
of the LEDs (the first packet probably prompts for a registry write
immediately, the color remains after power cycling the keyboard).
