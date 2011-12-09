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
    if not os.path.exists('png/{}'.format(day)):
        os.mkdir('png/{}'.format(day))
    png_file = 'png/{}.jpg'.format(timeid)
    page.save(png_file, quality=75)
    tools.print_image(png_file)

if __name__ == "__main__":
    if not tools.mount_camera():
        print 'Could not connect to camera. Try again.'
    for infile in os.listdir('infiles/'):
        timeid = time.strftime('%a/%H%M%S', time.localtime())
        process(infile, timeid)
        #os.rename('infiles/' + infile, 'outfiles/' + infile)
    if tools.umount_camera():
        print 'Finished. You can disconnect the camera now.'
    else:
        print 'Could not disconnect from camera. Please use the software safely remove function before disconnecting.'
