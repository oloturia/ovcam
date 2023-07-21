#!/usr/bin/env python3
from tkinter import *
from PIL import Image, ImageTk
import sys
import readYUV422
import threading
import logging

logging.basicConfig(level="INFO", format="%(name)s - %(levelname)s - %(message)s")
logging.debug("Starting...")

cam_width = 320  #Cam resolution
cam_height = 240
buffer_reg = {"RID":"","WID":"","VAL":""}

image_file = Image.new(mode="RGB", size = (cam_width, cam_height)) #Image init

window = Tk()               #Tkinter init
window.geometry("340x480")
window.title("OV7670")
colour = IntVar()

register_read_value = StringVar()

cam_frame = Frame(window,bd=1,height=cam_height,width=cam_width) #Frame init
cam_frame.place(x=10,y=10)

cam_label = Label(cam_frame) #Label init
cam_label.place(x=0,y=0)

input_read_frame = Frame(window,bd=1,height=110,width=310)
input_read_frame.place(x=0,y=290)

input_write_frame = Frame(window,bd=1,height=110 ,width=310)
input_write_frame.place(x=0,y=400)

input_switch_frame = Frame(window,bd=1,height=30, width=310)
input_switch_frame.place(x=0,y=260)

def alter_read_buffer():
	buffer_reg["RID"] = register_read_input.get()
	
def alter_write_buffer():
	buffer_reg["WID"] = register_write_input.get()
	buffer_reg["VAL"] = register_write_value.get()
	
label_read = Label(input_read_frame,text="Read register")
button_read = Button(input_read_frame,text="Read",command=alter_read_buffer)
register_read_input = Entry(input_read_frame)
register_read_output = Entry(input_read_frame,textvariable=register_read_value,state="readonly")

label_read.pack(side = TOP)
button_read.pack(side = RIGHT)
register_read_input.pack(side = TOP)
register_read_output.pack(side = TOP)

label_write = Label(input_write_frame,text="Write register")
button_write = Button(input_write_frame,text="Write",command=alter_write_buffer)
register_write_input = Entry(input_write_frame)
register_write_value = Entry(input_write_frame)

toggle_colours = Checkbutton(input_switch_frame,text="Colours",variable=colour,onvalue=1,offvalue=0)

label_write.pack(side = TOP)
button_write.pack(side = RIGHT)
register_write_input.pack(side = TOP)
register_write_value.pack(side = TOP)
toggle_colours.pack(side = TOP)


if len(sys.argv) == 2:    #Checks if user selected a different port
	port = sys.argv[1]
else:
	port = "/dev/ttyACM0" #Default port

def refreshImage(): #Threading
	global buffer_reg
	global cam_width
	global cam_height
	global port
	global register_read_value
	while True:
		
		if buffer_reg["RID"]:
			logging.debug("Read register")
			register_read_value.set(readYUV422.readImage(port_dev=port,regId=int(buffer_reg["RID"],16),colour=colour.get()))
			buffer_reg["RID"] = ""
		elif buffer_reg["WID"]:
			logging.debug("Write register")
			readYUV422.readImage(port_dev=port,regId=int(buffer_reg["WID"],16),regVal=int(buffer_reg["VAL"],16),colour=colour.get())
			buffer_reg["WID"] = ""
			buffer_reg["VAL"] = ""
		else:
			logging.debug("Image requested")
			bitmap = readYUV422.readImage(port_dev=port,width=cam_width,height=cam_height,colour=colour.get())
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
