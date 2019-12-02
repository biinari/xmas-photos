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

def create_title(base, group_name, day, timeid):
    day_timeid = day + '/' + timeid
    shadow = 2
    black = (0, 0, 0, 255)
    white = (255, 255, 255, 255)
    grey = (65, 90, 104, 255)
    draw = ImageDraw.Draw(base)
    group_font = ImageFont.truetype(os.path.join('fonts', 'DejaVuSans.ttf'), 120)
    small_font = ImageFont.truetype(os.path.join('fonts', 'DejaVuSans.ttf'), 42)
    textdraw = TextDraw(draw)
    group_rect = textdraw.centre(
        (1118, 158, 3053, 430),
        group_name, group_font)
    timeid_rect = textdraw.right(
        (886, 2339, 3215, 2393),
        day_timeid, small_font)
    textdraw.text(group_rect, group_name, black, group_font)
    textdraw.text(timeid_rect, day_timeid, grey, small_font, shadow, white)

# Process photo from +infile+
# - infile String Full path to input file
# - group_name String Name of the group of people in the photo
# - day String Day (3-letters) on which photo was processed
# - timeid String Identifier for photo
# - copies Int Number of copies to print
def process(infile, group_name, day, timeid, copies=1):
    mask = Mask((A4_WIDTH, A4_HEIGHT))
    page = mask.apply_mask(infile)
    create_title(page, group_name, day, timeid)
    tools.mkdir_p(os.path.join('png', day))
    png_file = os.path.join('png', day, '{}_{}.jpg'.format(timeid, tools.safe_filename(group_name)))
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
    names = os.listdir('infiles')
    names.sort()
    day = tools.get_day()
    tools.mkdir_p(os.path.join('outfiles', day))
    for infile in names:
        group_name = raw_input('Group name: ')
        timeid = time.strftime('%H%M%S', time.localtime())
        process(os.path.join('infiles', infile), group_name, day, timeid)
        outfile_name = '{}_{}.jpg'.format(timeid, tools.safe_filename(group_name))
        os.rename(os.path.join('infiles', infile),
                  os.path.join('outfiles', day, outfile_name))
    print 'Finished.'

if __name__ == "__main__":
    run()
