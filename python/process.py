#!/usr/bin/env python
# Process photos for Bowley Christmas Experience
import os, sys
import shutil
import Image, ImageFile
import ImageFont, ImageDraw
import math
from fade import Fade

def apply_mask(infile):
    try:
        photo = Image.open('infiles/' + infile)
    except IOError:
        print "Cannot open", infile
        return
    (width, height) = photo.size
    fade = Fade()
    try:
        mask = fade.getMask(width, height)
    except IOError:
        print "Cannot open mask file"
        return
    try:
        base = fade.getBase(width, height)
    except IOError:
        print "Cannot open base file"
        return
    base.paste(photo, (0, 0, width, height), mask)
    base.save('outfiles/' + infile, 'PNG')

def create_title(group_name):
    width = 600
    height = 200
    fade = Fade()
    base = Image.new('RGBA', (width, height))
    draw = ImageDraw.Draw(base)
    titleFont = ImageFont.truetype('fonts/BookmanDemi.pfb', 36)
    #smallFont = ImageFont.truetype('Helvetica', 10)
    #titleFont = ImageFont.truetype('/usr/local/share/fonts/BEAVER_LODGE.ttf', 36)
    draw.text((10, 10), "Christmas Experience", fill=(0,0,0,255), font=titleFont)
    base.save('fonttest.png')

def process(infile, group_name):
    apply_mask(infile)

if __name__ == "__main__":
    #for infile in os.listdir('infiles/'):
    #    process(infile, 'Test Group')
    create_title("Test Group")
