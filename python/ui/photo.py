import wx

class Photo(wx.StaticBitmap):

    path = None

    default_size = (600, 400)

    def __init__(self, *args, **kwargs):
        """ View a photo selected for processing. """
        kwargs['size'] = kwargs.get('size', self.default_size)
        wx.StaticBitmap.__init__(self, *args, **kwargs)
        self.load_blank()

    def load_from_file(self, name):
        """ Load Photo from filename. """
        image = wx.Image(name)
        (width, height) = self.GetSize()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.BitmapFromImage(image)
        self.SetBitmap(bitmap)
        self.path = name

    def load_blank(self):
        """ Load a blank image. """
        (width, height) = self.GetSize()
        image = wx.EmptyImage(width, height, True)
        bitmap = wx.BitmapFromImage(image)
        self.SetBitmap(bitmap)
        self.path = None

    def validate_image(self):
        """ Validate image is set. """
        valid = self.path != None and self.path != ''
        if not valid:
            wx.MessageBox("Please open an image", caption="No image open", parent=self.Parent)
        return valid
