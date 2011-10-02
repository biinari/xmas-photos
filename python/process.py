import os, sys
import shutil
import Image, ImageFile

def createMask(width, height):
    mask = Image.new('RGBA', (width, height))
    mask.save('mask/{0}x{1}.png'.format(width, height))

def createBase(width, height):
    base = Image.new('RGBA', (width, height), (255,255,255,255))
    base.save('base/{0}x{1}.png'.format(width, height))

for infile in os.listdir('infiles/'):
    try:
        photo = Image.open('infiles/' + infile)
    except IOError:
        print "Cannot open", infile
        break
    (width, height) = photo.size
    try:
        mask = Image.open('mask/{0}x{1}.png'.format(width, height))
    except IOError:
        print "cannot open mask file {0}x{1}.png".format(width, height)
        break
    try:
        base = Image.open('base/{0}x{1}.png'.format(width, height));
    except IOError:
        print "Cannot open base file {0}x{1}.png".format(width, height)
        break
    base.paste(photo, (0, 0, width, height), mask)
    base.save('outfiles/' + infile, 'PNG')