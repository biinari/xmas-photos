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

# Landscape at 300 ppi
a4width = 3508
a4height = 2480
a5width = 2480
a5height = 1754
camera_mount = '/mnt/camera'
do_camera = False
do_print = False

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

def get_left_rect(rect, draw, text, font):
    """ Get rectangle tuple to align text left, vertically centred. """
    (width, height) = draw.textsize(text, font=font)
    left = rect[0]
    top = (rect[3] - rect[1] - height) / 2 + rect[1]
    pos = (left, top, left + width, top + height)
    return pos

def draw_text(draw, rect, text, fill, font, shadow=None, shadowFill=None):
    if (shadow != None):
        draw.text((rect[0] + shadow, rect[1] + shadow),
                  text, fill=shadowFill, font=font)
    draw.text((rect[0], rect[1]), text, fill=fill, font=font)

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
    title_rect = get_centre_rect(
        (0, 0, page_size[0], photo_rect[1]),
        draw, title, titleFont)
    group_rect = get_centre_rect(
        (0, photo_rect[3], page_size[0], page_size[1] - (page_size[1] - photo_rect[3]) / 3),
        draw, group_name, groupFont)
    subtitle_rect = get_centre_rect(
        (0, group_rect[3], page_size[0], page_size[1] - margin),
        draw, subtitle, subtitleFont)
    timeid_rect = get_left_rect(
        (photo_rect[0], group_rect[3], page_size[0], page_size[1] - margin),
        draw, timeid, smallFont)
    copy_rect = get_right_rect(
        (0, group_rect[3], photo_rect[2], page_size[1] - margin),
        draw, copy, smallFont)
    draw_text(draw, title_rect, title, red, titleFont, shadow, darkred)
    draw_text(draw, group_rect, group_name, darkgreen, groupFont, shadow, green)
    draw_text(draw, subtitle_rect, subtitle, red, subtitleFont, shadow, darkred)
    draw_text(draw, timeid_rect, timeid, grey, smallFont)
    draw_text(draw, copy_rect, copy, grey, smallFont)

def process(infile, group_name, timeid):
    page = Image.new('RGBA', (a4width, a4height), (255,255,255,255))
    photo_size = (a4width * 3 / 4, a4height * 3 / 4)
    photo = apply_mask(infile, photo_size)
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
