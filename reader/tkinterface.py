#!/usr/bin/env python3
from tkinter import *
from PIL import Image, ImageTk
import sys
import readYUV422
import threading
import logging

logging.basicConfig(level="DEBUG", format="%(name)s - %(levelname)s - %(message)s")
logging.debug("Starting...")

cam_width = 320  #Cam resolution
cam_height = 240

image_file = Image.new(mode="RGB", size = (cam_width, cam_height)) #Image init

window = Tk()               #Tkinter init
window.geometry("340x460")
window.title("OV7670")

cam_frame = Frame(window,bd=1,height=cam_height,width=cam_width) #Frame init
cam_frame.place(x=10,y=10)
cam_frame.pack(side="top")

cam_label = Label(cam_frame) #Label init
cam_label.place(x=0,y=0)

if len(sys.argv) == 2:    #Checks if user selected a different port
	port = sys.argv[1]
else:
	port = "/dev/ttyACM0" #Default port

def refreshImage(): #Threading
	while True:
		logging.debug("Image requested")
		bitmap = readYUV422.readImage(port,cam_width,cam_height)
		index = 0
		for y in range(cam_height):
			for x in range(cam_width):
				image_file.putpixel((x, y), bitmap[index])
				index += 1
		logging.debug("Image received")
		photo = ImageTk.PhotoImage(image_file)
		cam_label.config(image = photo)

Refresh = threading.Thread(target=refreshImage, daemon=True).start()

window.mainloop()
