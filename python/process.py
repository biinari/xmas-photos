#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :
# Process photos for Bowley Christmas Experience
import os
import time

from PIL import ImageFont, ImageDraw

from mask import Mask
from textdraw import TextDraw
import tools

# Landscape at 300 ppi
A4_WIDTH = 3508
A4_HEIGHT = 2480

def create_title(base, group_name, timeid):
    shadow = 2
    black = (0, 0, 0, 255)
    white = (255, 255, 255, 255)
    grey = (65, 90, 104, 255)
    draw = ImageDraw.Draw(base)
    group_font = ImageFont.truetype('fonts/DejaVuSans.ttf', 120)
    small_font = ImageFont.truetype('fonts/DejaVuSans.ttf', 42)
    textdraw = TextDraw(draw)
    group_rect = textdraw.centre(
        (1118, 158, 3053, 430),
        group_name, group_font)
    timeid_rect = textdraw.right(
        (886, 2339, 3215, 2393),
        timeid, small_font)
    textdraw.text(group_rect, group_name, black, group_font)
    textdraw.text(timeid_rect, timeid, grey, small_font, shadow, white)

def process(infile, group_name, timeid, copies=1):
    mask = Mask((A4_WIDTH, A4_HEIGHT))
    page = mask.apply_mask(infile)
    create_title(page, group_name, timeid)
    day = tools.get_day()
    if not os.path.exists('png/{}'.format(day)):
        os.mkdir('png/{}'.format(day))
    png_file = 'png/{}_{}.jpg'.format(timeid, group_name.replace(' ', '_'))
    page.save(png_file, quality=75)
    tools.print_image(png_file, copies)

def run():
    if not tools.mount_camera():
        print 'Could not connect to camera. Try again.'
    tools.get_camera_files()
    if tools.umount_camera():
        print 'You can disconnect the camera now.'
    else:
        print 'Could not disconnect from camera.'
    names = os.listdir('infiles/')
    names.sort()
    day = tools.get_day()
    if not os.path.exists('outfiles/{}'.format(day)):
        os.mkdir('outfiles/{}'.format(day))
    for infile in names:
        group_name = raw_input('Group name: ')
        timeid = time.strftime('%a/%H%M%S', time.localtime())
        process(infile, group_name, timeid)
        os.rename('infiles/' + infile,
                  'outfiles/{}_{}.jpg'.format(timeid, group_name.replace(' ', '_')))
    print 'Finished.'

if __name__ == "__main__":
    run()
