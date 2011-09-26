import os, sys
import shutil
import Image, ImageFile

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
