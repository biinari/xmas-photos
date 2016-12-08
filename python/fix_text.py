#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :
# Process photos for Bowley Christmas Experience
import os

from PIL import Image
from PIL import ImageFont, ImageDraw

from textdraw import TextDraw
import tools

# Landscape at 300 ppi
A4_WIDTH = 3508
A4_HEIGHT = 2480
A5_WIDTH = 2480
A5_HEIGHT = 1754

def create_title(base, page_size, photo_rect, group_name):
    shadow = 2
    darkgreen = (41, 105, 13, 255)
    green = (67, 173, 22, 255)
    white = (255, 255, 255, 255)
    # margin = 48
    draw = ImageDraw.Draw(base)
    group_font = ImageFont.truetype('fonts/CooperBlackStd-Italic.otf', 120)
    textdraw = TextDraw(draw)
    group_rect = textdraw.centre(
        (0, photo_rect[3], page_size[0], page_size[1] - (page_size[1] - photo_rect[3]) / 3),
        group_name, group_font)
    # biggroup = (0, group_rect[1], page_size[0], group_rect[3])
    draw.rectangle(group_rect, fill=white)
    textdraw.text(group_rect, group_name, darkgreen, group_font, shadow, green)

def process(infile, group_name, timeid):
    page = Image.open('infiles/' + infile)
    photo_size = (A4_WIDTH * 3 / 4, A4_HEIGHT * 3 / 4)
    photo_left = (A4_WIDTH - photo_size[0]) / 2
    photo_top = (A4_HEIGHT - photo_size[1]) / 2 - A4_HEIGHT / 64
    photo_right = photo_left + photo_size[0]
    photo_bottom = photo_top + photo_size[1]
    photo_rect = (photo_left, photo_top, photo_right, photo_bottom)
    create_title(page, (A4_WIDTH, A4_HEIGHT), photo_rect, group_name)
    day = tools.get_day()
    if not os.path.exists('png/{}'.format(day)):
        os.mkdir('png/{}'.format(day))
    png_file = 'png/{}_{}.jpg'.format(timeid, tools.safe_filename(group_name))
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
        os.rename('infiles/' + infile,
                  'outfiles/{}_{}.jpg'.format(timeid, tools.safe_filename(group_name)))

if __name__ == "__main__":
    run()
