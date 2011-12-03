#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Process photos for Bowley Christmas Experience
import os, sys
import subprocess
import Image, ImageFile
import ImageFont, ImageDraw
import math
import time
from fade import Fade
from textdraw import TextDraw

# Landscape at 300 ppi
a4width = 3508
a4height = 2480
a5width = 2480
a5height = 1754
camera_mount = '/mnt/camera'
do_camera = False
do_print = False

def create_title(base, page_size, photo_size, photo_rect, group_name, timeid):
    title = "Christmas Experience"
    subtitle = "Bowley 2011"
    copy = u"© 2011 East Lancashire Scouts"
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
    page = Image.new('RGBA', (a4width, a4height), (255,255,255,255))
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
    day = time.strftime('%a', time.localtime())
    if not os.path.exists('png/{}'.format(day)):
        os.mkdir('png/{}'.format(day))
    png_file = 'png/{}_{}.png'.format(timeid, group_name.replace(' ','_'))
    page.save(png_file)
    if (do_print):
        print_image(png_file)

def mount_camera():
    if do_camera:
        if os.path.exists(camera_mount) and os.path.ismount(camera_mount):
            mounted = True
        else:
            mounted = not subprocess.call(['mount', camera_mount])
        return mounted
    else:
        return True

def umount_camera():
    if do_camera:
        if os.path.exists(camera_mount) and os.path.ismount(camera_mount):
            umounted = not subprocess.call(['umount', camera_mount])
        else:
            umounted = True
        return umounted
    else:
        return True

def print_image(filename):
    printer = 'Kodak-ESP-5250-wifi'
    success = not subprocess.call(['lp', '-d' + printer, '-o', 'media=a4', '-o', 'scaling=100', filename])
    return success

if __name__ == "__main__":
    if not mount_camera():
        print 'Could not connect to camera. Try again.'
    for infile in os.listdir('infiles/'):
        timeid = time.strftime('%a/%H%M%S', time.localtime())
        process(infile, 'Test Group', timeid)
        #os.rename('infiles/' + infile, 'outfiles/' + infile)
    if umount_camera():
        print 'Finished. You can disconnect the camera now.'
    else:
        print 'Could not disconnect from camera. Please use the software safely remove function before disconnecting.'
