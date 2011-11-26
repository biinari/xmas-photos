#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
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

def draw_text(draw, rect, text, fill, font, shadow=None, shadowFill=None):
    if (shadow != None):
        draw.text((rect[0] + shadow, rect[1] + shadow),
                  text, fill=shadowFill, font=font)
    draw.text((rect[0], rect[1]), text, fill=fill, font=font)

def create_title(base, page_size, photo_size, photo_rect, group_name):
    title = "Christmas Experience"
    subtitle = "Bowley 2011"
    copy = u"© 2011 East Lancashire Scouts"
    shadow = 2
    shadowFill = (0,255,0,255)
    fade = Fade()
    draw = ImageDraw.Draw(base)
    titleFont = ImageFont.truetype('fonts/BookmanDemi.pfb', 144)
    subtitleFont = ImageFont.truetype('fonts/BookmanDemi.pfb', 100)
    groupFont = ImageFont.truetype('fonts/CooperBlackStd-Italic.otf', 120)
    smallFont = ImageFont.truetype('fonts/DejaVuSans.ttf', 36)
    title_rect = get_centre_rect(
        (0, 0, page_size[0], photo_rect[1]),
        draw, title, titleFont)
    group_rect = get_centre_rect(
        (0, photo_rect[3], page_size[0], page_size[1] - (page_size[1] - photo_rect[3]) / 3),
        draw, group_name, groupFont)
    subtitle_rect = get_centre_rect(
        (0, group_rect[3], page_size[0], page_size[1]),
        draw, subtitle, subtitleFont)
    copy_rect = get_right_rect(
        (0, group_rect[3], photo_rect[2], page_size[1]),
        draw, group_name, smallFont)
    draw_text(draw, title_rect, title, (255,0,0,255), titleFont,
              shadow, shadowFill)
    draw_text(draw, group_rect, group_name, (0,0,0,255), groupFont)
    draw_text(draw, subtitle_rect, subtitle, (255,0,0,255),
              subtitleFont, shadow, shadowFill)
    draw_text(draw, copy_rect, copy, (65,90,104,255), smallFont)

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
