#!/usr/bin/env python3
from tkinter import *
from PIL import Image, ImageTk
import sys
import readYUV422

cam_width = 240
cam_height = 320

if len(sys.argv) == 2:
	port = sys.argv[1]
else:
	port = "/dev/ttyACM0"


window = Tk()
window.geometry("340x460")
window.title("OV7670")

cam_window = Frame(window,bd=0,height=cam_height,width=cam_width)
cam_window.place(x=10,y=10)
cam_window.pack(side="top")

cam_image = Image.new(mode="RGB", size = (cam_width, cam_height))

def refreshImage(display_width,display_height,port,image):
	bitmap = readYUV422.readImage(port,display_width,display_height)
	index = 0
	for y in range(display_height):
		for y in range(display_width):
			image.putpixel((x, y), bitmap[index])
			index += 1
	window.event_generate("<<Refreshed>>")
	return image

def refreshHandler(event):
	cam_image = refreshImage(cam_width,cam_height,port,cam_image)

window.bind("<<Refreshed>>", refreshHandler)
cam_window.image = cam_image

window.mainloop()
