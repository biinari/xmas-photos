import wx

class Photo(wx.StaticBitmap):

    path = None

    default_size = (600, 400)

    """ View a photo selected for processing. """
    def __init__(self, *args, **kwargs):
        kwargs['size'] = kwargs.get('size', self.default_size)
        wx.StaticBitmap.__init__(self, *args, **kwargs)
        self.LoadBlank()

    """ Load Photo from filename. """
    def LoadFromFile(self, name):
        image = wx.Image(name)
        (width, height) = self.GetSize()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.BitmapFromImage(image)
        self.SetBitmap(bitmap)
        self.path = name

    """ Load a blank image. """
    def LoadBlank(self):
        (width, height) = self.GetSize()
        bitmap = wx.EmptyBitmap(width, height)
        self.SetBitmap(bitmap)
        self.path = None

    """ Validate image is set. """
    def ValidateImage(self):
        valid = self.path != None and self.path != ''
        if not valid:
            wx.MessageBox("Please open an image", caption="No image open", parent=self.Parent)
        return valid

