#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Calendar layout for Saturday at Bowley Christmas Experience
import os
import Image, ImageFile
import ImageFont, ImageDraw
import math
import time
from fade import Fade
from textdraw import TextDraw
import tools

# Portrait at 300 ppi
a4width = 2480
a4height = 3508

def create_title(base, page_size, photo_size, photo_rect, timeid):
    title = "Christmas Experience"
    subtitle = "December - 2011"
    copy = u"© 2011 East Lancashire Scouts"
    shadow = 2
    darkred = (176, 7, 7, 255)
    red = (238, 9, 9, 255)
    darkgreen = (41, 105, 13, 255)
    green = (67, 173, 22, 255)
    black = (0, 0, 0, 255)
    grey = (65, 90, 104, 255)
    margin = 48
    cal_top = 2100
    cal_bottom = 3350
    fade = Fade()
    draw = ImageDraw.Draw(base)
    #titleFont = ImageFont.truetype('fonts/BookmanDemi.pfb', 144)
    subtitleFont = ImageFont.truetype('fonts/BookmanDemi.pfb', 120)
    #groupFont = ImageFont.truetype('fonts/CooperBlackStd-Italic.otf', 120)
    smallFont = ImageFont.truetype('fonts/DejaVuSans.ttf', 42)
    textdraw = TextDraw(draw)
    #title_rect = textdraw.centre(
    #    (0, margin * 2, page_size[0], photo_rect[1] / 2),
    #    title, titleFont)
    #group_rect = textdraw.centre(
    #    (0, photo_rect[1] / 2, page_size[0], photo_rect[1]),
    #    group_name, groupFont)
    subtitle_rect = textdraw.centre(
        (0, photo_rect[3], page_size[0], cal_top),
        subtitle, subtitleFont)
    timeid_rect = textdraw.left(
        (photo_rect[0], cal_bottom, page_size[0], page_size[1] - margin),
        timeid, smallFont)
    copy_rect = textdraw.right(
        (0, cal_bottom, photo_rect[2], page_size[1] - margin),
        copy, smallFont)
    #textdraw.text(title_rect, title, red, titleFont, shadow, darkred)
    #textdraw.text(group_rect, group_name, darkgreen, groupFont, shadow, green)
    textdraw.text(subtitle_rect, subtitle, red, subtitleFont, shadow, darkred)
    textdraw.text(timeid_rect, timeid, grey, smallFont)
    textdraw.text(copy_rect, copy, grey, smallFont)

def process(infile, timeid):
    try:
        page = Image.open('base/Calendar_2011.png')
    except IOError:
        print "Cannot open calendar page base"
        return
    photo_size = (a4width * 3 / 4, a4height * 3 / 8)
    fade = Fade()
    photo = fade.applyMask(infile, photo_size)
    photo_left = (a4width - photo_size[0]) / 2
    photo_top = 520
    photo_right = photo_left + photo_size[0]
    photo_bottom = photo_top + photo_size[1]
    photo_rect = (photo_left, photo_top, photo_right, photo_bottom)
    page.paste(photo, photo_rect)
    create_title(page, (a4width, a4height), photo_size, photo_rect, timeid)
    day = time.strftime('%a', time.localtime())
    if not os.path.exists('png/{}'.format(day)):
        os.mkdir('png/{}'.format(day))
    png_file = 'png/{}.jpg'.format(timeid)
    page.save(png_file, quality=75)
    tools.print_image(png_file)

def run():
    if not tools.mount_camera():
        print 'Could not connect to camera. Try again.'
    tools.get_camera_files()
    if tools.umount_camera():
        print 'You can disconnect the camera now.'
    else:
        print 'Could not disconnect from camera. Please use the software safely remove function before disconnecting.'
    names = os.listdir('infiles/')
    names.sort()
    for infile in names:
        #group_name = raw_input('Group name: ')
        timeid = time.strftime('%a/%H%M%S', time.localtime())
        process(infile, timeid)
        os.rename('infiles/' + infile, 'outfiles/{}.jpg'.format(timeid))
    print "Finished."

if __name__ == "__main__":
    run()
