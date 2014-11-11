class TextDraw(object):
    draw = None

    def __init__(self, draw):
        self.draw = draw

    def centre(self, rect, text, font):
        """ Get rectangle tuple to draw the text centred. """
        (width, height) = self.draw.textsize(text, font=font)
        left = (rect[2] - rect[0] - width) / 2 + rect[0]
        top = (rect[3] - rect[1] - height) / 2 + rect[1]
        pos = (left, top, left + width, top + height)
        return pos

    def right(self, rect, text, font):
        """ Get rectangle tuple to align text right, vertically centred. """
        (width, height) = self.draw.textsize(text, font=font)
        left = rect[2] - width
        top = (rect[3] - rect[1] - height) / 2 + rect[1]
        pos = (left, top, left + width, top + height)
        return pos

    def left(self, rect, text, font):
        """ Get rectangle tuple to align text left, vertically centred. """
        (width, height) = self.draw.textsize(text, font=font)
        left = rect[0]
        top = (rect[3] - rect[1] - height) / 2 + rect[1]
        pos = (left, top, left + width, top + height)
        return pos

    def text(self, rect, text, fill, font, shadow=None, shadow_fill=None):
        if shadow != None:
            self.draw.text((rect[0] + shadow, rect[1] + shadow),
                           text, fill=shadow_fill, font=font)
        self.draw.text((rect[0], rect[1]), text, fill=fill, font=font)
