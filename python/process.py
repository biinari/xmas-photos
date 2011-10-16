#!/usr/bin/env python
# Process photos for Bowley Christmas Experience
import os, sys
import shutil
import Image, ImageFile
import math
from fade import Fade

def process():
    for infile in os.listdir('infiles/'):
        try:
            photo = Image.open('infiles/' + infile)
        except IOError:
            print "Cannot open", infile
            break
        (width, height) = photo.size
        fade = Fade();
        try:
            mask = fade.getMask(width, height)
        except IOError:
            print "Cannot open mask file"
            break
        try:
            base = fade.getBase(width, height)
        except IOError:
            print "Cannot open base file"
            break
        base.paste(photo, (0, 0, width, height), mask)
        base.save('outfiles/' + infile, 'PNG')

fade = Fade()
fade.createMask(2272,1704)
