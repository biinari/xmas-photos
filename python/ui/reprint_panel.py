import wx
from ui.photo import Photo
import reprint

class ReprintPanel(wx.Panel):

    """ Panel to find and reprint photos already processed. """
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.CreateWidgets()

    def CreateWidgets(self):
        vert = wx.BoxSizer(wx.VERTICAL)
        horiz = wx.BoxSizer(wx.HORIZONTAL)
        self.staticImage = Photo(self)
        self.numCopiesLabel = wx.StaticText(self, label="Number of copies:")
        self.numCopies = wx.TextCtrl(self)
        self.reprintBtn = wx.Button(self, label="Reprint")

        self.Bind(wx.EVT_BUTTON, self.OnReprint, self.reprintBtn)

        horiz.Add(self.numCopiesLabel, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        horiz.Add(self.numCopies, 1, wx.ALIGN_CENTER_VERTICAL)
        horiz.Add(self.reprintBtn, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        vert.Add(self.staticImage, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 5)
        vert.Add(horiz, 1, wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(vert)
        self.Centre()

    def OnReprint(self, event):
        if self.staticImage.ValidateImage() and self.ValidateNumCopies:
            numCopies = self.numCopies.GetValue()
            if numCopies != '':
                reprint.reprint(self.filename, int(numCopies))
            else:
                reprint.reprint(self.filename)

    def ValidateNumCopies(self):
        numCopies = self.numCopies.GetValue()
        valid = numCopies == "" or numCopies.isdigit()
        if not valid:
            wx.MessageBox("Integer required",
                          caption="Number of copies must be an integer")
        return valid
