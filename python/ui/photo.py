import wx

class Photo(wx.StaticBitmap):

    path = None

    default_size = (600, 400)

    """ View a photo selected for processing. """
    def __init__(self, *args, **kwargs):
        kwargs['size'] = kwargs.get('size', self.default_size)
        wx.StaticBitmap.__init__(self, *args, **kwargs)

    """ Load Photo from filename. """
    def LoadFromFile(self, name):
        image = wx.Image(name)
        (width, height) = self.GetSize()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.BitmapFromImage(image)
        self.SetBitmap(bitmap)
        self.path = name

    """ Validate image is set. """
    def ValidateImage(self):
        valid = self.infile != None and self.infile != ''
        if valid:
            wx.MessageBox("Please open an image", caption="No image open", parent=self.parent)
        return valid

