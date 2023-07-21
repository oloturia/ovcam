# ovcam
A small interface for interfacing an Arduino Due with a OV7670.

Working only with an Arduino Due at the moment, mainly because Uno and smaller MC don't have enough SRAM for an entire image, and I don't have yet figured out how to split the transmission in an efficient way. For the same reason, the framerate is quite slow. Besides, Due has 3.3v logic levels so there is no need for voltage splitters.

The output of the cam is: Cb0 Y0 Cr0 Y1 Cb2 Y2 Cr2 Y3 Cb4 Y4 Cr4... 
Y=luma, Cb=blue chroma, Cr=red chroma. Chroma red is the difference between red and the colour perceived by the sensor, Chroma blue it's the same with blue. For example, if Cr and Cb are zero, the colour would be green. Luma is the luminance, if we use Y instead of R G B in a pixel, the image will be rendered in black and white.

Y, Cb and Cr are 1 byte and they are transmitted by the pins D0-D7 on each PCLK rising. As the Due can store only Y OR CbCr, it sends two scans: first the luma and then the chroma. A small script in python fetch the two scans and translate them in an RGB image. Timing is fundamental, that's why it's important to use the native USB port of the Due, which is faster than the programming one.

Python scripts need some libraries

showYUV422.py <port, default /dev/ttyACM0>

shows the image with: pygame 

saveYUV422.py -p <port default /dev/ttyACM0> -f <filename default out.png>

save an image with: PIL

tkinterface.py <port, default /dev/ttyACM0>

is a small interface made with: Tkinter

it shows the image and has two inputs -
 read accepts one hexadecimal number in format 0x00, it queries a register of the OV7670
 write accepts two hex numbers, it writes a value in a register

OV7670 wiring with Due is shown in the #define section before the code except for the I²C pins:

SDA --> SIOD

SCL --> SIOC

Also PWDN should be connected to GND. PWDN places the cam in standby if it's 1 (+3.3v) and wakes it up if it's 0 (0v).
