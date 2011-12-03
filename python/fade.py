import Image, ImageFile
import math

class Fade:
    """Manages mask and base for fade border"""

    def applyMask(self, infile, size):
        (width, height) = size
        try:
            photo = Image.open('infiles/' + infile)
        except IOError:
            print "Cannot open", infile
            return
        photo = photo.resize(size, Image.NEAREST)
        try:
            mask = self.getMask(width, height)
        except IOError:
            print "Cannot open mask file"
            return
        try:
            base = self.getBase(width, height)
        except IOError:
            print "Cannot open base file"
            return
        base.paste(photo, (0, 0, width, height), mask)
        return base

    def maskPixel(self, row, col, width, height):
        exp = 48
        val = (1 - (2.0 * col / width - 1) ** exp) * (1 - (2.0 * row / height - 1) ** exp)
        return int(math.floor(255 * val))

    def createMask(self, width, height):
        mask = Image.new('RGBA', (width, height))
        data = []
        for row in range(height):
            for col in range(width):
                data.append((255, 255, 255,
                             self.maskPixel(row, col, width, height)))
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

if __name__ == "__main__":
    """ Create a mask in the size we want as preparation. """
    fade = Fade()
    fade.createMask(2272,1704)
