import os

import wx

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
        open_row = wx.BoxSizer(wx.HORIZONTAL)
        action_row = wx.BoxSizer(wx.HORIZONTAL)
        open_btn = wx.Button(self, label="Open")
        self.static_image = Photo(self)
        num_copies_label = wx.StaticText(self, label="Number of copies:")
        self.num_copies = wx.TextCtrl(self)
        self.num_copies.SetValue("1")
        reprint_btn = wx.Button(self, label="Reprint")

        self.Bind(wx.EVT_BUTTON, self.on_open, open_btn)
        self.Bind(wx.EVT_BUTTON, self.on_reprint, reprint_btn)

        open_row.Add(open_btn, 1, wx.ALIGN_CENTER_VERTICAL)

        action_row.Add(num_copies_label, 1, wx.ALIGN_CENTER_VERTICAL)
        action_row.Add(wx.Size(10, 10))
        action_row.Add(self.num_copies, 1, wx.ALIGN_CENTER_VERTICAL)
        action_row.Add(wx.Size(20, 10))
        action_row.Add(reprint_btn, 1, wx.ALIGN_CENTER_VERTICAL)

        vert.Add(wx.Size(10, 10))
        vert.Add(open_row, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vert.Add(wx.Size(10, 10))
        vert.Add(self.static_image, 1, wx.SHAPED | wx.ALIGN_CENTER)
        vert.Add(wx.Size(10, 10))
        vert.Add(action_row, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vert.Add(wx.Size(10, 10))
        self.SetSizer(vert)
        self.Centre()

    def on_open(self, event_):
        cwd = os.getcwd()
        day = tools.get_day()
        initial_dir = os.path.join(cwd, 'png/{}'.format(day))
        if not os.path.exists(initial_dir):
            initial_dir = os.path.join(cwd, 'png')
            if not os.path.exists(initial_dir):
                os.mkdir(initial_dir)
        dlg = wx.lib.imagebrowser.ImageDialog(self, initial_dir)
        dlg.Centre()
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFile()
            self.static_image.load_from_file(self.filename)
        dlg.Destroy()

    def on_reprint(self, event_):
        if self.validate():
            num_copies = self.num_copies.GetValue()
            if num_copies != '':
                reprint.reprint(self.filename, int(num_copies))
            else:
                reprint.reprint(self.filename)

    def validate(self):
        return self.static_image.validate_image() \
            and self.validate_num_copies

    def validate_num_copies(self):
        num_copies = self.num_copies.GetValue()
        valid = num_copies == "" or num_copies.isdigit()
        if not valid:
            wx.MessageBox("Integer required",
                          caption="Number of copies must be an integer")
        return valid
