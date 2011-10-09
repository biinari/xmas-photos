#!/usr/bin/env python
# Process photos for Bowley Christmas Experience
import os, sys
import shutil
import Image, ImageFile
import math

class Fade:
"""Manages mask and base for fade border"""

    def maskPixel(self, row, col, width, height):
        exp = 24
        val = (1 - (2.0 * col / width - 1) ** exp) * (1 - (2.0 * row / height - 1) ** exp)
        return int(math.floor(255 * val))

    def createMask(self, width, height):
        mask = Image.new('LA', (width, height))
        data = []
        for row in range(height):
            for col in range(width):
                data.append(maskPixel(row, col, width, height))
        data = zip(data, map(lambda x: 255, range(height*width)))
        mask.putdata(data)
        mask.save('mask/{0}x{1}.png'.format(width, height))
        return mask

    def _getMask(self, width, height):
        return Image.open('mask/{0}x{1}.png'.format(width, height))

    def getMask(self, width, height):
        try:
            mask = self._getMask(width, height)
        except IOError:
            mask = self.createMask(width, height)
        return mask

    def createBase(self, width, height):
        base = Image.new('RGBA', (width, height), (255,255,255,255))
        base.save('base/{0}x{1}.png'.format(width, height))
        return base

    def _getBase(self, width, height):
        return Image.open('base/{0}x{1}.png'.format(width, height));

    def getBase(self, width, height):
        try:
            base = self._getBase(width, height)
        except IOError:
            base = self.createBase(width, height)
        return base


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
