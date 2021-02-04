#!/usr/bin/python3

import pygame
import pygame.gfxdraw
import sys
import signal

import readYUV422

def signal_handler(sig,frame):
		pygame.quit()
		sys.exit(0)
		
signal.signal(signal.SIGINT, signal_handler)

pygame.init()
display_width = 320
display_height = 240
image = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Image")

if len(sys.argv) == 2:
	port = sys.argv[1]
else:
	port = "/dev/ttyACM0"


def showImage():
	index = 0
	bitmap = readYUV422.readImage(port,display_width,display_height)
	for y in range(display_height):
			for x in range(display_width):
				pygame.gfxdraw.pixel(image, x, y, bitmap[index])
				index += 1
	pygame.display.update()
	
while True:
	showImage()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
