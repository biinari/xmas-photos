import wx
import os
from ui.photo import Photo
import reprint
import tools

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

    def OnOpen(self, event):
        cwd = os.getcwd()
        day = tools.get_day()
        initial_dir = os.path.join(cwd, 'png/{}'.format(day))
        dlg = wx.lib.imagebrowser.ImageDialog(self, initial_dir)
        dlg.Centre()
        if dlg.ShowModal() == wx.ID_OK:
            self.staticImage.LoadFromFile(dlg.GetFile())
        dlg.Destroy()

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
