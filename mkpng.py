#!/bin/python2.7

import os, sys, re
from PIL import Image, ImageChops, ImageOps

def show_usage () :
	print("""Simple JPEG to monitor sized wallpaper generator\nDeps: PIL(2.7)\nUsage:\n[python2.7] %s /path/to/image [/path/to/outfile] [WIDTHxHEIGHT]\n""" % (sys.argv[0],))

def makeThumb(f_in, f_out, size=(80,80), pad=False):
	image = Image.open(f_in)
	image.thumbnail(size, Image.ANTIALIAS)
	image_size = image.size

	if pad:
		thumb = image.crop( (0, 0, size[0], size[1]) )
		offset_x = max( (size[0] - image_size[0]) / 2, 0 )
		offset_y = max( (size[1] - image_size[1]) / 2, 0 )
		thumb = ImageChops.offset(thumb, offset_x, offset_y)
	else:
		thumb = ImageOps.fit(image, size, Image.ANTIALIAS, (0.5, 0.5))
		thumb.save(f_out)

def main () :
	if len(sys.argv)>1 and os.path.isfile(sys.argv[1]) :
		infile = sys.argv[1]
		outfile = sys.argv[2] if len(sys.argv)>2 else os.path.splitext(infile)[0] + ".png"
		if(len(sys.argv)>3) :
			width, height = [ int(s) for s in re.split(r'[xX]', sys.argv[3])]
		else :
			screen = os.popen("xrandr -q -d :0").readlines()[0]
			height=int(screen.split()[9][:-1])
			width=int(screen.split()[7])

		print(infile, outfile)
		print(unicode(width) + "x" + unicode(height))
		makeThumb(infile, outfile, (width, height), False)
	else :
		show_usage()

if __name__ == "__main__" : 
	main()
