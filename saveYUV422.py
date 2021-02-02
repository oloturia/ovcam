#!/usr/bin/python3

import readYUV422
import sys
from PIL import Image
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-p','--port',metavar='port',default='/dev/ttyACM0',nargs=1,type=str,help='serial port')
parser.add_argument('-f','--filename',metavar='filename',default="out.png",nargs=1,type=str,help='file name')
args = parser.parse_args()

fileDir = os.path.dirname(os.path.abspath(__file__))
display_width = 320
display_height = 240


port = args.port
index = 0
bitmap = readYUV422.readImage(port,display_width,display_height)
image = Image.new(mode="RGB", size = (display_width,display_height))

for y in range(display_height):
		for x in range(display_width):
			image.putpixel((x, y), bitmap[index])
			index += 1
image.save(fileDir+"/"+args.filename)

print("DONE")

