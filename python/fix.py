#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :
# Process photos for Bowley Christmas Experience
import os
import Image, ImageFile
import ImageFont, ImageDraw
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
    title = "Christmas Experience"
    subtitle = "Bowley 2012"
    copy = u"© 2012 East Lancashire Scouts"
    shadow = 2
    darkred = (176, 7, 7, 255)
    red = (238, 9, 9, 255)
    darkgreen = (41, 105, 13, 255)
    green = (67, 173, 22, 255)
    black = (0, 0, 0, 255)
    grey = (65, 90, 104, 255)
    margin = 48
    fade = Fade()
    draw = ImageDraw.Draw(base)
    titleFont = ImageFont.truetype('fonts/BookmanDemi.pfb', 144)
    subtitleFont = ImageFont.truetype('fonts/BookmanDemi.pfb', 100)
    groupFont = ImageFont.truetype('fonts/CooperBlackStd-Italic.otf', 120)
    smallFont = ImageFont.truetype('fonts/DejaVuSans.ttf', 42)
    textdraw = TextDraw(draw)
    title_rect = textdraw.centre(
        (0, 0, page_size[0], photo_rect[1]),
        title, titleFont)
    group_rect = textdraw.centre(
        (0, photo_rect[3], page_size[0], page_size[1] - (page_size[1] - photo_rect[3]) / 3),
        group_name, groupFont)
    subtitle_rect = textdraw.centre(
        (0, group_rect[3], page_size[0], page_size[1] - margin),
        subtitle, subtitleFont)
    timeid_rect = textdraw.left(
        (photo_rect[0], group_rect[3], page_size[0], page_size[1] - margin),
        timeid, smallFont)
    copy_rect = textdraw.right(
        (0, group_rect[3], photo_rect[2], page_size[1] - margin),
        copy, smallFont)
    textdraw.text(title_rect, title, red, titleFont, shadow, darkred)
    textdraw.text(group_rect, group_name, darkgreen, groupFont, shadow, green)
    textdraw.text(subtitle_rect, subtitle, red, subtitleFont, shadow, darkred)
    textdraw.text(timeid_rect, timeid, grey, smallFont)
    textdraw.text(copy_rect, copy, grey, smallFont)

def process(infile, group_name, timeid):
    page = Image.new('RGB', (a4width, a4height), (255,255,255,255))
    photo_size = (a4width * 3 / 4, a4height * 3 / 4)
    fade = Fade()
    photo = fade.applyMask(infile, photo_size)
    photo_left = (a4width - photo_size[0]) / 2
    photo_top = (a4height - photo_size[1]) / 2 - a4height / 64
    photo_right = photo_left + photo_size[0]
    photo_bottom = photo_top + photo_size[1]
    photo_rect = (photo_left, photo_top, photo_right, photo_bottom)
    page.paste(photo, photo_rect)
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
        #timeid = time.strftime('%a/%H%M%S', time.localtime())
        process(infile, group_name, timeid)
        os.rename('infiles/' + infile, 'outfiles/{}_{}.jpg'.format(timeid, group_name.replace(' ','_')))

if __name__ == "__main__":
    run()
