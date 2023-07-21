#!/usr/bin/python3

import pygame
import pygame.gfxdraw
import sys
import signal
import readYUV422
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-p','--port',metavar='port',default='/dev/ttyACM0',type=str,help='serial port')
parser.add_argument('-c','--colour',action='store_true',help='enable colours')
args = parser.parse_args()

port = args.port
colSelect = 1 if args.colour else 0


def signal_handler(sig,frame):
		pygame.quit()
		sys.exit(0)
		
signal.signal(signal.SIGINT, signal_handler)

pygame.init()
display_width = 320
display_height = 240
image = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Image")




def showImage():
	index = 0
	bitmap = readYUV422.readImage(port_dev=port,width=display_width,height=display_height,colour=colSelect)
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
