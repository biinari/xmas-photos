#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :
# Process photos for Bowley Christmas Experience
import os
from PIL import Image
from PIL import ImageFont, ImageDraw
from fade import Fade
from textdraw import TextDraw
import tools

# Landscape at 300 ppi
A4_WIDTH = 3508
A4_HEIGHT = 2480
A5_WIDTH = 2480
A5_HEIGHT = 1754

def create_title(base, page_size, photo_rect, group_name, timeid):
    title = "Christmas Experience"
    subtitle = "Bowley 2014"
    copy = u"© 2014 East Lancashire Scouts"
    shadow = 2
    darkred = (176, 7, 7, 255)
    red = (238, 9, 9, 255)
    darkgreen = (41, 105, 13, 255)
    green = (67, 173, 22, 255)
    # black = (0, 0, 0, 255)
    grey = (65, 90, 104, 255)
    margin = 48
    draw = ImageDraw.Draw(base)
    title_font = ImageFont.truetype('fonts/BookmanDemi.pfb', 144)
    subtitle_font = ImageFont.truetype('fonts/BookmanDemi.pfb', 100)
    group_font = ImageFont.truetype('fonts/CooperBlackStd-Italic.otf', 120)
    small_font = ImageFont.truetype('fonts/DejaVuSans.ttf', 42)
    textdraw = TextDraw(draw)
    title_rect = textdraw.centre(
        (0, 0, page_size[0], photo_rect[1]),
        title, title_font)
    group_rect = textdraw.centre(
        (0, photo_rect[3], page_size[0], page_size[1] - (page_size[1] - photo_rect[3]) / 3),
        group_name, group_font)
    subtitle_rect = textdraw.centre(
        (0, group_rect[3], page_size[0], page_size[1] - margin),
        subtitle, subtitle_font)
    timeid_rect = textdraw.left(
        (photo_rect[0], group_rect[3], page_size[0], page_size[1] - margin),
        timeid, small_font)
    copy_rect = textdraw.right(
        (0, group_rect[3], photo_rect[2], page_size[1] - margin),
        copy, small_font)
    textdraw.text(title_rect, title, red, title_font, shadow, darkred)
    textdraw.text(group_rect, group_name, darkgreen, group_font, shadow, green)
    textdraw.text(subtitle_rect, subtitle, red, subtitle_font, shadow, darkred)
    textdraw.text(timeid_rect, timeid, grey, small_font)
    textdraw.text(copy_rect, copy, grey, small_font)

def process(infile, group_name, timeid):
    page = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    photo_size = (A4_WIDTH * 3 / 4, A4_HEIGHT * 3 / 4)
    fade = Fade()
    photo = fade.apply_mask(infile, photo_size)
    photo_left = (A4_WIDTH - photo_size[0]) / 2
    photo_top = (A4_HEIGHT - photo_size[1]) / 2 - A4_HEIGHT / 64
    photo_right = photo_left + photo_size[0]
    photo_bottom = photo_top + photo_size[1]
    photo_rect = (photo_left, photo_top, photo_right, photo_bottom)
    page.paste(photo, photo_rect)
    create_title(page, (A4_WIDTH, A4_HEIGHT), photo_rect, group_name, timeid)
    day = tools.get_day()
    if not os.path.exists('png/{}'.format(day)):
        os.mkdir('png/{}'.format(day))
    png_file = 'png/{}_{}.jpg'.format(timeid, group_name.replace(' ', '_'))
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
        os.rename('infiles/' + infile,
                  'outfiles/{}_{}.jpg'.format(timeid, group_name.replace(' ', '_')))

if __name__ == "__main__":
    run()
