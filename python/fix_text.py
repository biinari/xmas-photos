#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :
# Process photos for Bowley Christmas Experience
import os
from PIL import Image, ImageFile
from PIL import ImageFont, ImageDraw
import math
import time
from fade import Fade
from textdraw import TextDraw
import tools

# Landscape at 300 ppi
a4width = 3508
a4height = 2480
a5width = 2480
a5height = 1754

def create_title(base, page_size, photo_size, photo_rect, group_name, timeid):
    shadow = 2
    darkgreen = (41, 105, 13, 255)
    green = (67, 173, 22, 255)
    white = (255, 255, 255, 255)
    margin = 48
    fade = Fade()
    draw = ImageDraw.Draw(base)
    groupFont = ImageFont.truetype('fonts/CooperBlackStd-Italic.otf', 120)
    textdraw = TextDraw(draw)
    group_rect = textdraw.centre(
        (0, photo_rect[3], page_size[0], page_size[1] - (page_size[1] - photo_rect[3]) / 3),
        group_name, groupFont)
    biggroup = (0, group_rect[1], page_size[0], group_rect[3])
    draw.rectangle(group_rect, fill=white)
    textdraw.text(group_rect, group_name, darkgreen, groupFont, shadow, green)

def process(infile, group_name, timeid):
    page = Image.open('infiles/' + infile)
    photo_size = (a4width * 3 / 4, a4height * 3 / 4)
    fade = Fade()
    photo_left = (a4width - photo_size[0]) / 2
    photo_top = (a4height - photo_size[1]) / 2 - a4height / 64
    photo_right = photo_left + photo_size[0]
    photo_bottom = photo_top + photo_size[1]
    photo_rect = (photo_left, photo_top, photo_right, photo_bottom)
    create_title(page, (a4width, a4height), photo_size, photo_rect, group_name, timeid)
    day = tools.get_day()
    if not os.path.exists('png/{}'.format(day)):
        os.mkdir('png/{}'.format(day))
    png_file = 'png/{}_{}.jpg'.format(timeid, group_name.replace(' ','_'))
    page.save(png_file, quality=75)
    tools.print_image(png_file)

def run():
    names = os.listdir('infiles/')
    names.sort()
    for infile in names:
        day = tools.get_day()
        timeid = day + '/' + raw_input('Time id: ')
        group_name = raw_input('Group name: ')
        process(infile, group_name, timeid)
        os.rename('infiles/' + infile, 'outfiles/{}_{}.jpg'.format(timeid, group_name.replace(' ','_')))

if __name__ == "__main__":
    run()
