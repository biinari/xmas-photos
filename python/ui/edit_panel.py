import os
import shutil
import time

import wx

from ui.photo import Photo
import process
import tools

class EditPanel(wx.Panel):

    filename = None

    """ Panel to find and edit photos already processed. """
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        vert = wx.BoxSizer(wx.VERTICAL)
        open_row = wx.BoxSizer(wx.HORIZONTAL)
        name_row = wx.BoxSizer(wx.HORIZONTAL)
        bottom_row = wx.BoxSizer(wx.HORIZONTAL)
        open_btn = wx.Button(self, label="Open")
        restore_btn = wx.Button(self, label="Restore Discarded")
        self.static_image = Photo(self)
        group_label = wx.StaticText(self, label="Group Name:")
        self.group_name = wx.TextCtrl(self)
        keep_timeid_label = wx.StaticText(self, label="Keep day/time ID?")
        self.keep_timeid = wx.CheckBox(self)
        num_copies_label = wx.StaticText(self, label="Number of copies:")
        self.num_copies = wx.TextCtrl(self)
        self.num_copies.SetValue("1")
        process_label = tools.DO_PRINT and "Print" or "Process"
        process_btn = wx.Button(self, label=process_label)

        self.Bind(wx.EVT_BUTTON, self.on_open, open_btn)
        self.Bind(wx.EVT_BUTTON, self.on_restore, restore_btn)
        self.Bind(wx.EVT_BUTTON, self.on_process, process_btn)

        open_row.Add(open_btn, 1, wx.ALIGN_CENTER_VERTICAL)
        open_row.Add(wx.Size(10, 10))
        open_row.Add(restore_btn, 2, wx.ALIGN_CENTER_VERTICAL)

        name_row.Add(group_label, 1, wx.ALIGN_CENTER_VERTICAL)
        name_row.Add(wx.Size(10, 10))
        name_row.Add(self.group_name, 4, wx.ALIGN_CENTER_VERTICAL)

        bottom_row.Add(num_copies_label, 1, wx.ALIGN_CENTER_VERTICAL)
        bottom_row.Add(wx.Size(10, 10))
        bottom_row.Add(self.num_copies, 0, wx.ALIGN_CENTER_VERTICAL)
        bottom_row.Add(wx.Size(20, 10))
        bottom_row.Add(keep_timeid_label, 1, wx.ALIGN_CENTER_VERTICAL)
        bottom_row.Add(wx.Size(10, 10))
        bottom_row.Add(self.keep_timeid, 0, wx.ALIGN_CENTER_VERTICAL)
        bottom_row.Add(wx.Size(20, 10))
        bottom_row.Add(process_btn, 1, wx.ALIGN_CENTER_VERTICAL)

        vert.Add(wx.Size(10, 10))
        vert.Add(open_row, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vert.Add(wx.Size(10, 10))
        vert.Add(self.static_image, 1, wx.SHAPED | wx.ALIGN_CENTER)
        vert.Add(wx.Size(10, 10))
        vert.Add(name_row, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vert.Add(wx.Size(10, 10))
        vert.Add(bottom_row, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vert.Add(wx.Size(10, 10))
        self.SetSizer(vert)
        self.Centre()

    def on_open(self, _event):
        cwd = os.getcwd()
        day = tools.get_day()
        initial_dir = os.path.join(cwd, 'outfiles', day)
        if not os.path.exists(initial_dir):
            initial_dir = os.path.join(cwd, 'outfiles')
            tools.mkdir_p(initial_dir)
        dlg = wx.lib.imagebrowser.ImageDialog(self, initial_dir)
        dlg.Centre()
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFile()
            self.static_image.load_from_file(self.filename)
        dlg.Destroy()

    def on_restore(self, _event):
        cwd = os.getcwd()
        day = tools.get_day()
        initial_dir = os.path.join(cwd, 'discard', day)
        if not os.path.exists(initial_dir):
            initial_dir = os.path.join(cwd, 'discard')
            tools.mkdir_p(initial_dir)
        dlg = wx.lib.imagebrowser.ImageDialog(self, initial_dir)
        dlg.Centre()
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFile()
            self.static_image.load_from_file(self.filename)
        dlg.Destroy()

    def on_process(self, _event):
        if self.validate():
            if self.keep_timeid.GetValue():
                day = os.path.basename(os.path.dirname(self.filename))
                timeid = os.path.basename(self.filename)[0:6]
            else:
                day = tools.get_day()
                timeid = time.strftime('%H%M%S', time.localtime())
            infile = self.filename
            group_name = self.group_name.GetValue()
            num_copies = self.num_copies.GetValue()
            if num_copies != '':
                process.process(infile, group_name, day, timeid, int(num_copies)) # pylint: disable=too-many-function-args
            else:
                process.process(infile, group_name, day, timeid)
            out_name = '{}_{}.jpg'.format(timeid, tools.safe_filename(group_name))
            out_path = os.path.join('outfiles', day, out_name)
            shutil.copyfile(self.filename, out_path)

    def validate(self):
        return self.static_image.validate_image() \
            and self.validate_group_name() \
            and self.validate_num_copies()

    def validate_group_name(self):
        name = self.group_name.GetValue()
        valid = name != ''
        if not valid:
            wx.MessageBox("Please enter group name",
                          caption="Group name is missing")
        return valid

    def validate_num_copies(self):
        num_copies = self.num_copies.GetValue()
        valid = num_copies == "" or num_copies.isdigit()
        if not valid:
            wx.MessageBox("Integer required",
                          caption="Number of copies must be an integer")
        return valid
