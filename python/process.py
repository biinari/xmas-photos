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

def apply_mask(infile, size):
    (width, height) = size
    try:
        photo = Image.open('infiles/' + infile)
    except IOError:
        print "Cannot open", infile
        return
    photo = photo.resize(size, Image.NEAREST)
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

def get_centre_rect(rect, draw, text, font):
    """ Get rectangle tuple to draw the text centred. """
    (width, height) = draw.textsize(text, font=font)
    left = (rect[2] - rect[0] - width) / 2 + rect[0]
    top = (rect[3] - rect[1] - height) / 2 + rect[1]
    pos = (left, top, left + width, top + height)
    return pos

def get_right_rect(rect, draw, text, font):
    """ Get rectangle tuple to align text right, vertically centred. """
    (width, height) = draw.textsize(text, font=font)
    left = rect[2] - width
    top = (rect[3] - rect[1] - height) / 2 + rect[1]
    pos = (left, top, left + width, top + height)
    return pos

def create_title(base, page_size, photo_size, photo_rect, group_name):
    title = "Christmas Experience"
    subtitle = "Bowley 2011"
    fade = Fade()
    draw = ImageDraw.Draw(base)
    titleFont = ImageFont.truetype('fonts/BookmanDemi.pfb', 144)
    smallFont = ImageFont.truetype('fonts/DejaVuSans.ttf', 36)
    title_rect = get_centre_rect(
        (0, 0, page_size[0], photo_rect[1]),
        draw, title, titleFont)
    subtitle_rect = get_centre_rect(
        (0, photo_rect[3], page_size[0], page_size[1] - (page_size[1] - photo_rect[3]) / 3),
        draw, subtitle, titleFont)
    group_name_rect = get_right_rect(
        (0, subtitle_rect[3], photo_rect[2], page_size[1]),
        draw, group_name, smallFont)
    draw.text((title_rect[0] + 2, title_rect[1] + 2), title, fill=(0,255,0,255), font=titleFont)
    draw.text((title_rect[0], title_rect[1]), title, fill=(255,0,0,255), font=titleFont)
    draw.text((subtitle_rect[0] + 2, subtitle_rect[1] + 2), subtitle, fill=(0,255,0,255), font=titleFont)
    draw.text((subtitle_rect[0], subtitle_rect[1]), subtitle, fill=(255,0,0,255), font=titleFont)
    draw.text((group_name_rect[0], group_name_rect[1]), group_name, fill=(0,0,0,255), font=smallFont)

def process(infile, group_name):
    page = Image.new('RGBA', (a4width, a4height), (255,255,255,255))
    photo_size = (a4width * 3 / 4, a4height * 3 / 4)
    photo = apply_mask(infile, photo_size)
    photo_left = (a4width - photo_size[0]) / 2
    photo_top = (a4height - photo_size[1]) / 2 - a4height / 64
    photo_right = photo_left + photo_size[0]
    photo_bottom = photo_top + photo_size[1]
    photo_rect = (photo_left, photo_top, photo_right, photo_bottom)
    page.paste(photo, photo_rect)
    create_title(page, (a4width, a4height), photo_size, photo_rect, group_name)
    page.save('page.png')

if __name__ == "__main__":
    for infile in os.listdir('infiles/'):
        process(infile, 'Test Group')
