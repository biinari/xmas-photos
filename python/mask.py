import os

from PIL import Image

class Mask(object):
    """Manages mask for page"""

    PHOTO_WIDTH = 2400
    PHOTO_HEIGHT = 1800
    PHOTO_LEFT = 852
    PHOTO_TOP = 468

    def __init__(self, paper_size):
        (self.paper_width, self.paper_height) = paper_size

    def apply_mask(self, infile):
        photo_right = self.PHOTO_LEFT + self.PHOTO_WIDTH
        photo_bottom = self.PHOTO_TOP + self.PHOTO_HEIGHT
        photo_rect = (self.PHOTO_LEFT, self.PHOTO_TOP, photo_right, photo_bottom)

        page = self.get_page()
        photo = self.get_photo(infile)
        mask = self.get_mask()
        page.paste(photo, photo_rect)
        page.paste(mask, (0, 0, self.paper_width, self.paper_height), mask)
        return page

    def get_photo(self, infile):
        photo = Image.open(infile)
        photo = photo.resize((self.PHOTO_WIDTH, self.PHOTO_HEIGHT), Image.NEAREST)
        return photo

    # raises IOError
    @staticmethod
    def get_mask():
        return Image.open(os.path.join('mask', 'christmas_mask_2017.png'))

    def get_page(self):
        return Image.new(
            'RGB',
            (self.paper_width, self.paper_height),
            (255, 255, 255, 255))
