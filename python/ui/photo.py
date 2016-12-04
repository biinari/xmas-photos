import wx

class Photo(wx.StaticBitmap):

    path = None

    DEFAULT_SIZE = (600, 400)

    def __init__(self, *args, **kwargs):
        """ View a photo selected for processing. """
        kwargs['size'] = kwargs.get('size', self.DEFAULT_SIZE)
        wx.StaticBitmap.__init__(self, *args, **kwargs)
        self.SetMinSize(self.DEFAULT_SIZE)
        self.load_blank()

        self.Bind(wx.EVT_SIZE, self.on_size)

    def load_from_file(self, name):
        """ Load Photo from filename. """
        self.image = wx.Image(name)
        (width, height) = self.best_size()
        scaled_image = self.image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        self.draw_image(scaled_image)
        self.path = name

    def load_blank(self):
        """ Load a blank image. """
        (width, height) = self.GetClientSize()
        scaled_image = self.image = wx.EmptyImage(width, height, True)
        self.draw_image(scaled_image)
        self.path = None

    def validate_image(self):
        """ Validate image is set. """
        valid = self.path != None and self.path != ''
        if not valid:
            wx.MessageBox("Please open an image", caption="No image open", parent=self.Parent)
        return valid

    def best_size(self):
        (image_width, image_height) = self.image.GetSize()
        (width, height) = self.GetClientSize()

        if image_width < self.DEFAULT_SIZE[0] or image_height < self.DEFAULT_SIZE[1]:
            return (self.DEFAULT_SIZE[0], self.DEFAULT_SIZE[1])
        if width < self.DEFAULT_SIZE[0] or height < self.DEFAULT_SIZE[1]:
            return (self.DEFAULT_SIZE[0], self.DEFAULT_SIZE[1])

        image_ratio = 1.0 * image_width / image_height
        ratio = 1.0 * width / height
        if ratio > image_ratio:
            width = int(round(height * image_ratio))
        elif ratio < image_ratio:
            height = int(round(width / image_ratio))
        return (width, height)

    def draw_image(self, scaled_image):
        bitmap = wx.BitmapFromImage(scaled_image)
        self.SetBitmap(bitmap)

    def on_size(self, event_):
        (width, height) = self.best_size()
        scaled_image = self.image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        self.draw_image(scaled_image)
