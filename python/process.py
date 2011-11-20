#!/usr/bin/env python
# Process photos for Bowley Christmas Experience
import os, sys
import shutil
import Image, ImageFile
import ImageFont, ImageDraw
import math
from fade import Fade

# Landscape at 300 ppi
a4width = 3508
a4height = 2480
a5width = 2480
a5height = 1754

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
    return base

def get_centre_left(image_width, draw, text, font):
    """ Get left coordinate to draw the text centred. """
    (width, height) = draw.textsize(text, font=font)
    left = (image_width - width) / 2
    return left

def create_title(base, width, height, group_name):
    title = "Christmas Experience"
    subtitle = "Bowley 2011"
    fade = Fade()
    draw = ImageDraw.Draw(base)
    titleFont = ImageFont.truetype('fonts/BookmanDemi.pfb', 144)
    smallFont = ImageFont.truetype('fonts/DejaVuSans.ttf', 20)
    title_left = get_centre_left(width, draw, title, titleFont)
    subtitle_left = get_centre_left(width, draw, subtitle, titleFont)
    group_name_left = get_centre_left(width, draw, group_name, smallFont)
    draw.text((title_left + 1, 22), title, fill=(0,255,0,255), font=titleFont)
    draw.text((title_left, 20), title, fill=(255,0,0,255), font=titleFont)
    draw.text((subtitle_left + 1, 2002), subtitle, fill=(0,255,0,255), font=titleFont)
    draw.text((subtitle_left, 2000), subtitle, fill=(255,0,0,255), font=titleFont)
    draw.text((group_name_left, 2250), group_name, fill=(0,0,0,255), font=smallFont)
    base.save('fonttest.png')

def process(infile, group_name):
    page = Image.new('RGBA', (a4width, a4height), (255,255,255,255))
    photo = apply_mask(infile)
    photo_left = (a4width - photo.size[0]) / 2
    photo_top = (a4height - photo.size[1]) / 2
    page.paste(photo, (photo_left, photo_top,
                       photo_left + photo.size[0], photo_top + photo.size[1]))
    create_title(page, a4width, a4height, group_name)
    page.save('page.png')

if __name__ == "__main__":
    for infile in os.listdir('infiles/'):
        process(infile, 'Test Group')
