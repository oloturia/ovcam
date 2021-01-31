import serial
import math
import pygame
import pygame.gfxdraw
import time

pygame.init()

display_width = 320
display_height = 240

image = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Image")

ser = serial.Serial('/dev/ttyACM0', 460800*2)
data = ser.read(size=display_width*display_height)
index = 0

Y = []
Cb = []
Cr = []
alt = True

for index,byte in enumerate(data):
	if (index % 2) == 0:
		Y.append(byte)
	elif alt:
		Cb.append(byte)
		alt = False
	else:
		Cr.append(byte)
		alt = True

indexY = 0
indexCb = 0.
indexCr = 0.

for y in range(display_height):
	for x in range(display_width):
		Y = data[indexY]
		Cb = data[math.floor(indexCb)]
		Cr = data[math.floor(indexCr)]
		R = max(0, min(255, 1.164*(Y - 16) + 1.596*(Cr - 128)))
		G = max(0, min(255, 1.164*(Y - 16) - 0.813*(Cr - 128) - 0.391*(Cb - 128)))
		B = max(0, min(255, 1.164*(Y - 16) + 2.018*(Cr - 128)))
		pygame.gfxdraw.pixel(image, x, y, (R,G,B))
#		pygame.gfxdraw.pixel(image, x, y, (Y,Y,Y))
		indexY += 1
		indexCb += 0.5
		indexCr += 0.5

pygame.display.update()
print("DONE")
time.sleep(10)
