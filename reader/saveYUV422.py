#!/usr/bin/python3

import readYUV422
import sys
from PIL import Image
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-p','--port',metavar='port',default='/dev/ttyACM0',type=str,help='serial port')
parser.add_argument('-f','--filename',metavar='filename',default="out.png",type=str,help='file name')
parser.add_argument('-c','--colour',action='store_true',help='enable colours')
args = parser.parse_args()

fileDir = os.path.dirname(os.path.abspath(__file__))
display_width = 320
display_height = 240


port = args.port
colSelect = 1 if args.colour else 0
index = 0
bitmap = readYUV422.readImage(port_dev=port,width=display_width,height=display_height,colour=colSelect)
image = Image.new(mode="RGB", size = (display_width,display_height))

for y in range(display_height):
		for x in range(display_width):
			image.putpixel((x, y), bitmap[index])
			index += 1
image.save(fileDir+"/"+args.filename)

print("DONE")

