#!/usr/bin/python3

import serial
import math
import time


def readImage(port,width,height):
	ser = serial.Serial(port, 460800)
	ser.write(b"*")

	dataY = ser.read(size=width*height)
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

	bitmap = list()

	for y in range(height):
		for x in range(width):
			Y = dataY[index]
			Cb = dataCb[index]
			Cr = dataCr[index]

			R = int(max(0, min(255,Y + 1.40200 * (Cr -0x80))))
			G = int(max(0, min(255,Y - 0.34414 * (Cb - 0x80) - 0.71414 * (Cr - 0x80))))
			B = int(max(0, min(255,Y + 1.77200 * (Cb - 0x80))))
			bitmap.append((R,G,B))
			index += 1

	ser.flushInput()
	ser.close()
	return bitmap
