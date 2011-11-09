#!/usr/bin/env python
# Process photos for Bowley Christmas Experience
import os, sys
import shutil
import Image, ImageFile
import math
from fade import Fade

def process(infile, group_name):
    try:
        photo = Image.open('infiles/' + infile)
    except IOError:
        print "Cannot open", infile
        return
    (width, height) = photo.size
    fade = Fade();
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
    base.save('outfiles/' + infile, 'PNG')

if __name__ == "__main__":
    for infile in os.listdir('infiles/'):
        process(infile, 'Test Group')
