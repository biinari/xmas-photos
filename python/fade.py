import math

from PIL import Image

class Fade(object):
    """Manages mask and base for fade border"""

    def apply_mask(self, infile, size):
        (width, height) = size
        try:
            photo = Image.open('infiles/' + infile)
        except IOError:
            print "Cannot open", infile
            return
        photo = photo.resize(size, Image.NEAREST)
        try:
            mask = self.get_mask(width, height)
        except IOError:
            print "Cannot open mask file"
            return
        try:
            base = self.get_base(width, height)
        except IOError:
            print "Cannot open base file"
            return
        base.paste(photo, (0, 0, width, height), mask)
        return base

    @staticmethod
    def mask_pixel(row, col, width, height):
        exp = 48
        val = (1 - (2.0 * col / width - 1) ** exp) * (1 - (2.0 * row / height - 1) ** exp)
        return int(math.floor(255 * val))

    def create_mask(self, width, height):
        mask = Image.new('RGBA', (width, height))
        data = []
        for row in range(height):
            for col in range(width):
                data.append((255, 255, 255,
                             self.mask_pixel(row, col, width, height)))
        mask.putdata(data)
        mask.save('mask/{0}x{1}.png'.format(width, height))
        return mask

    @staticmethod
    def _get_mask(width, height):
        return Image.open('mask/{0}x{1}.png'.format(width, height))

    def get_mask(self, width, height):
        try:
            mask = self._get_mask(width, height)
        except IOError:
            mask = self.create_mask(width, height)
        return mask

    @staticmethod
    def create_base(width, height):
        base = Image.new('RGBA', (width, height), (255, 255, 255, 255))
        base.save('base/{0}x{1}.png'.format(width, height))
        return base

    @staticmethod
    def _get_base(width, height):
        return Image.open('base/{0}x{1}.png'.format(width, height))

    def get_base(self, width, height):
        try:
            base = self._get_base(width, height)
        except IOError:
            base = self.create_base(width, height)
        return base

def main():
    """ Create a mask in the size we want as preparation. """
    fade = Fade()
    fade.create_mask(2272, 1704)

if __name__ == "__main__":
    main()
