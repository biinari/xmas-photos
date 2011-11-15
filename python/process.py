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

def get_centre_left(image_width, draw, text, font):
    """ Get left coordinate to draw the text centred. """
    (width, height) = draw.textsize(text, font=font)
    left = (image_width - width) / 2
    return left

def create_title(group_name):
    width = 600
    height = 200
    title = "Christmas Experience"
    subtitle = "Bowley 2011"
    fade = Fade()
    base = Image.new('RGBA', (width, height), (255,255,255,255))
    draw = ImageDraw.Draw(base)
    titleFont = ImageFont.truetype('fonts/BookmanDemi.pfb', 36)
    smallFont = ImageFont.truetype('fonts/DejaVuSans.ttf', 10)
    title_left = get_centre_left(width, draw, title, titleFont)
    subtitle_left = get_centre_left(width, draw, subtitle, titleFont)
    group_name_left = get_centre_left(width, draw, group_name, smallFont)
    draw.text((title_left + 1, 11), title, fill=(0,255,0,255), font=titleFont)
    draw.text((title_left, 10), title, fill=(255,0,0,255), font=titleFont)
    draw.text((subtitle_left + 1, 51), subtitle, fill=(0,255,0,255), font=titleFont)
    draw.text((subtitle_left, 50), subtitle, fill=(255,0,0,255), font=titleFont)
    draw.text((group_name_left, 100), group_name, fill=(0,0,0,255), font=smallFont)
    base.save('fonttest.png')

def process(infile, group_name):
    apply_mask(infile)

if __name__ == "__main__":
    #for infile in os.listdir('infiles/'):
    #    process(infile, 'Test Group')
    create_title("Test Group")
