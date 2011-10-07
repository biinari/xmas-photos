#!/usr/bin/env python
# Process photos for Bowley Christmas Experience
import os, sys
import shutil
import Image, ImageFile
import math

def maskPixel(row, col, width, height):
    exp = 24
    val = (1 - pow((2.0 * col / width - 1), exp)) * (1 - pow((2.0 * row / height - 1), exp))
    return int(math.floor(255 * val))

def createMask(width, height):
    mask = Image.new('LA', (width, height))
    data = []
    for row in range(height):
        for col in range(width):
            data.append(maskPixel(row, col, width, height))
    data = zip(data, map(lambda x: 255, range(height*width)))
    mask.putdata(data)
    mask.save('mask/{0}x{1}.png'.format(width, height))

def createBase(width, height):
    base = Image.new('RGBA', (width, height), (255,255,255,255))
    base.save('base/{0}x{1}.png'.format(width, height))

def process():
    for infile in os.listdir('infiles/'):
        try:
            photo = Image.open('infiles/' + infile)
        except IOError:
            print "Cannot open", infile
            break
        (width, height) = photo.size
        try:
            mask = Image.open('mask/{0}x{1}.png'.format(width, height))
        except IOError:
            print "cannot open mask file {0}x{1}.png".format(width, height)
            break
        try:
            base = Image.open('base/{0}x{1}.png'.format(width, height));
        except IOError:
            print "Cannot open base file {0}x{1}.png".format(width, height)
            break
        base.paste(photo, (0, 0, width, height), mask)
        base.save('outfiles/' + infile, 'PNG')

createMask(2272,1704)
