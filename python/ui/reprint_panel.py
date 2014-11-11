import wx
import os
from ui.photo import Photo
import reprint
import tools

class ReprintPanel(wx.Panel):

    filename = None

    """ Panel to find and reprint photos already processed. """
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        vert = wx.BoxSizer(wx.VERTICAL)
        horiz = wx.BoxSizer(wx.HORIZONTAL)
        self.open_btn = wx.Button(self, label="Open")
        self.static_image = Photo(self)
        self.num_copies_label = wx.StaticText(self, label="Number of copies:")
        self.num_copies = wx.TextCtrl(self)
        self.reprint_btn = wx.Button(self, label="Reprint")

        self.Bind(wx.EVT_BUTTON, self.on_open, self.open_btn)
        self.Bind(wx.EVT_BUTTON, self.on_reprint, self.reprint_btn)

        horiz.Add(self.num_copies_label, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        horiz.Add(self.num_copies, 1, wx.ALIGN_CENTER_VERTICAL)
        horiz.Add(self.reprint_btn, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        vert.Add(self.open_btn, 1, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL)
        vert.Add(self.static_image, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 5)
        vert.Add(horiz, 1, wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(vert)
        self.Centre()

    def on_open(self, event_):
        cwd = os.getcwd()
        day = tools.get_day()
        initial_dir = os.path.join(cwd, 'png/{}'.format(day))
        dlg = wx.lib.imagebrowser.ImageDialog(self, initial_dir)
        dlg.Centre()
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFile()
            self.static_image.load_from_file(self.filename)
        dlg.Destroy()

    def on_reprint(self, event_):
        if self.static_image.validate_image() and self.validate_num_copies:
            num_copies = self.num_copies.GetValue()
            if num_copies != '':
                reprint.reprint(self.filename, int(num_copies))
            else:
                reprint.reprint(self.filename)

    def validate_num_copies(self):
        num_copies = self.num_copies.GetValue()
        valid = num_copies == "" or num_copies.isdigit()
        if not valid:
            wx.MessageBox("Integer required",
                          caption="Number of copies must be an integer")
        return valid
