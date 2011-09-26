import os, sys
import shutil
import Image, ImageFile

width = 2272
height = 1704

try:
    maskimage = Image.open('mask/{0}x{1}.png'.format(width, height))
except IOError:
    print "cannot open mask file {0}x{1}.png".format(width, height)

for infile in os.listdir('infiles/'):
    white = Image.new('RGBA', (width, height), (255,255,255,255))
    try:
        inimage = Image.open('infiles/' + infile)
    except IOError:
        print "Cannot open", infile
    white.paste(inimage, (0, 0, width, height), maskimage)
    white.save('outfiles/' + infile, 'PNG')
