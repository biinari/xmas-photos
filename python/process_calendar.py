#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :
# Calendar layout for Saturday at Bowley Christmas Experience
import os
import time

from PIL import Image
from PIL import ImageFont, ImageDraw

from fade import Fade
from textdraw import TextDraw
import tools

# Portrait at 300 ppi
A4_WIDTH = 2480
A4_HEIGHT = 3508

def create_title(base, page_size, photo_rect, day, timeid):
    year = tools.get_year()
    day_timeid = day + '/' + timeid
    # title = "Christmas Experience"
    subtitle = "December - {}".format(year)
    copy = u"© {} East Lancashire Scouts".format(year)
    shadow = 2
    darkred = (176, 7, 7, 255)
    red = (238, 9, 9, 255)
    # darkgreen = (41, 105, 13, 255)
    # green = (67, 173, 22, 255)
    # black = (0, 0, 0, 255)
    grey = (65, 90, 104, 255)
    margin = 48
    cal_top = 2100
    cal_bottom = 3350
    draw = ImageDraw.Draw(base)
    #titleFont = ImageFont.truetype(os.path.join('fonts', 'BookmanDemi.pfb'), 144)
    subtitle_font = ImageFont.truetype(os.path.join('fonts', 'BookmanDemi.pfb'), 120)
    #groupFont = ImageFont.truetype(os.path.join('fonts', 'CooperBlackStd-Italic.otf'), 120)
    small_font = ImageFont.truetype(os.path.join('fonts', 'DejaVuSans.ttf'), 42)
    textdraw = TextDraw(draw)
    #title_rect = textdraw.centre(
    #    (0, margin * 2, page_size[0], photo_rect[1] / 2),
    #    title, titleFont)
    #group_rect = textdraw.centre(
    #    (0, photo_rect[1] / 2, page_size[0], photo_rect[1]),
    #    group_name, groupFont)
    subtitle_rect = textdraw.centre(
        (0, photo_rect[3], page_size[0], cal_top),
        subtitle, subtitle_font)
    timeid_rect = textdraw.left(
        (photo_rect[0], cal_bottom, page_size[0], page_size[1] - margin),
        day_timeid, small_font)
    copy_rect = textdraw.right(
        (0, cal_bottom, photo_rect[2], page_size[1] - margin),
        copy, small_font)
    #textdraw.text(title_rect, title, red, titleFont, shadow, darkred)
    #textdraw.text(group_rect, group_name, darkgreen, groupFont, shadow, green)
    textdraw.text(subtitle_rect, subtitle, red, subtitle_font, shadow, darkred)
    textdraw.text(timeid_rect, day_timeid, grey, small_font)
    textdraw.text(copy_rect, copy, grey, small_font)

def process(infile, day, timeid):
    try:
        page = Image.open(os.path.join('base', 'Calendar_2014.png'))
    except IOError:
        print "Cannot open calendar page base"
        return
    photo_size = (A4_WIDTH * 3 / 4, A4_HEIGHT * 3 / 8)
    fade = Fade()
    photo = fade.apply_mask(infile, photo_size)
    photo_left = (A4_WIDTH - photo_size[0]) / 2
    photo_top = 520
    photo_right = photo_left + photo_size[0]
    photo_bottom = photo_top + photo_size[1]
    photo_rect = (photo_left, photo_top, photo_right, photo_bottom)
    page.paste(photo, photo_rect)
    create_title(page, (A4_WIDTH, A4_HEIGHT), photo_rect, day, timeid)
    tools.mkdir_p(os.path.join('png', day))
    png_file = os.path.join('png', day, '{}.jpg'.format(timeid))
    page.save(png_file, quality=75)
    tools.print_image(png_file)

def run():
    if not tools.mount_camera():
        print 'Could not connect to camera. Try again.'
    tools.get_camera_files()
    if tools.umount_camera():
        print 'You can disconnect the camera now.'
    else:
        print 'Could not disconnect from camera. Please use the software ' \
              'safely remove function before disconnecting.'
    names = os.listdir('infiles')
    names.sort()
    for infile in names:
        day = tools.get_day()
        #group_name = raw_input('Group name: ')
        timeid = time.strftime('%H%M%S', time.localtime())
        process(infile, day, timeid)
        outfile_name = '{}.jpg'.format(timeid)
        os.rename(os.path.join('infiles', infile),
                  os.path.join('outfiles', day, outfile_name))
    print "Finished."

if __name__ == "__main__":
    run()
