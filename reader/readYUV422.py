#!/usr/bin/python3

import serial
import math
import time
import logging


def readImage(port_dev,width=320,height=240,regId=0xD0,regVal=0xD0,colour=0):
	regCol = 0x01 if colour else 0x00
	ser = serial.Serial(port_dev, 8000000)
	ser.flushInput()
	ser.write(bytearray([regId,regVal,regCol]))
	
	if regId == 0xD0 and regVal == 0xD0:
		bitmap = list()
		dataY = ser.read(size=width*height)
		if colour:
			dataCbCr = ser.read(size=width*height)
			index = 0
			dataCb = list()
			dataCr = list()
			Alt = True

			for chroma in dataCbCr:
				if Alt:
					dataCr.extend([chroma,chroma])
					Alt = False
				else:
					dataCb.extend([chroma,chroma])
					Alt = True



			for y in range(height):
				for x in range(width):
					Y = dataY[index]
					Cb = dataCb[index]
					Cr = dataCr[index]

					R = int(max(0, min(255,Y + 1.40200 * (Cr - 0x80))))
					G = int(max(0, min(255,Y - 0.34414 * (Cb - 0x80) - 0.71414 * (Cr - 0x80))))
					B = int(max(0, min(255,Y + 1.77200 * (Cb - 0x80))))
					bitmap.append((R,G,B))
					index += 1
		else:
			index = 0
			for y in range(height):
				for x in range(width):
					R = G = B = int(dataY[index])
					bitmap.append((R,G,B))
					index +=1
		ser.close()
		print(index)
		return bitmap
	elif regId != 0xD0 and regVal == 0xD0:
		value = ser.read(1)
		return hex(ord(value))



