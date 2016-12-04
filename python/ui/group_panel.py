import os
import shutil
import time

import wx

from ui.photo import Photo
import process
import tools

class GroupPanel(wx.Panel):

    """ Files in infiles/ for choosing from (just the basenames) """
    names = []
    """ Current index into self.names """
    index = 0

    """ Panel to select and process photo """
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        vert = wx.BoxSizer(wx.VERTICAL)
        top_row = wx.BoxSizer(wx.HORIZONTAL)
        name_row = wx.BoxSizer(wx.HORIZONTAL)
        bottom_row = wx.BoxSizer(wx.HORIZONTAL)
        get_photos_btn = wx.Button(self, label="Get Photos")
        self.discard_btn = wx.Button(self, label="Discard")
        self.discard_btn.Disable()

        self.prev_btn = wx.Button(self, label="<")
        self.prev_btn.Disable()
        self.static_image = Photo(self)
        self.next_btn = wx.Button(self, label=">")
        self.next_btn.Disable()

        group_label = wx.StaticText(self, label="Group Name:")
        self.group_name = wx.TextCtrl(self)
        num_copies_label = wx.StaticText(self, label="Number of copies:")
        self.num_copies = wx.TextCtrl(self)
        self.num_copies.SetValue("1")
        process_btn = wx.Button(self, label="Print")

        self.Bind(wx.EVT_BUTTON, self.on_get_photos, get_photos_btn)
        self.Bind(wx.EVT_BUTTON, self.on_discard, self.discard_btn)
        self.Bind(wx.EVT_BUTTON, self.on_previous, self.prev_btn)
        self.Bind(wx.EVT_BUTTON, self.on_next, self.next_btn)
        self.Bind(wx.EVT_BUTTON, self.on_process, process_btn)

        top_row.Add(self.prev_btn, 1)
        top_row.Add(get_photos_btn, 2)
        top_row.Add(self.next_btn, 1)
        top_row.Add(wx.Size(20, 10))
        top_row.Add(self.discard_btn, 2)

        name_row.Add(group_label, 1, wx.ALIGN_CENTER_VERTICAL)
        name_row.Add(wx.Size(10, 10))
        name_row.Add(self.group_name, 4, wx.ALIGN_CENTER_VERTICAL)

        bottom_row.Add(num_copies_label, 1, wx.ALIGN_CENTER_VERTICAL)
        bottom_row.Add(wx.Size(10, 10))
        bottom_row.Add(self.num_copies, 1, wx.ALIGN_CENTER_VERTICAL)
        bottom_row.Add(wx.Size(20, 10))
        bottom_row.Add(process_btn, 1, wx.ALIGN_CENTER_VERTICAL)

        vert.Add(wx.Size(10, 10))
        vert.Add(top_row, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vert.Add(wx.Size(10, 10))
        vert.Add(self.static_image, 1, wx.SHAPED | wx.ALIGN_CENTER)
        vert.Add(wx.Size(10, 10))
        vert.Add(name_row, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vert.Add(wx.Size(10, 10))
        vert.Add(bottom_row, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vert.Add(wx.Size(10, 10))
        self.SetSizer(vert)
        self.Centre()

    def load_image(self, index):
        self.index = index
        self.static_image.load_from_file('infiles/' + self.names[index])
        self.discard_btn.Enable()
        if index >= len(self.names) - 1:
            self.next_btn.Disable()
        else:
            self.next_btn.Enable()
        if index == 0:
            self.prev_btn.Disable()
        else:
            self.prev_btn.Enable()

    def load_next_image(self):
        del self.names[self.index]
        if len(self.names) > self.index:
            self.load_image(self.index)
        elif len(self.names) > 0:
            self.load_image(len(self.names) - 1)
        else:
            self.load_blank()

    def load_blank(self):
        self.static_image.load_blank()
        self.discard_btn.Disable()

    def on_next(self, event_):
        if self.index + 1 < len(self.names):
            self.load_image(self.index + 1)

    def on_previous(self, event_):
        if self.index > 0:
            self.load_image(self.index - 1)

    def on_open(self, event_):
        cwd = os.getcwd()
        initial_dir = os.path.join(cwd)
        dlg = wx.lib.imagebrowser.ImageDialog(self, initial_dir)
        dlg.Centre()
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetFile()
            name = os.path.basename(path)
            shutil.copyfile(path, 'infiles/' + name)
            self.names.append(name)
            self.load_image(len(self.names) - 1)
        dlg.Destroy()

    def on_process(self, event_):
        if self.validate():
            timeid = time.strftime('%a/%H%M%S', time.localtime())
            infile = self.names[self.index]
            group_name = self.group_name.GetValue()
            num_copies = self.num_copies.GetValue()
            if num_copies != '':
                process.process(infile, group_name, timeid, int(num_copies))
            else:
                process.process(infile, group_name, timeid)
            os.rename('infiles/' + infile,
                      'outfiles/{}_{}.jpg'.format(timeid, group_name.replace(' ', '_')))
            self.load_next_image()

    def on_get_photos(self, event_):
        if not tools.mount_camera():
            self.SetStatusText('Could not connect to camera. Try again.')
        tools.get_camera_files()
        if tools.umount_camera():
            self.SetStatusText('You can disconnect the camera now.')
        else:
            self.SetStatusText('Could not disconnect from camera.')
        names = os.listdir('infiles/')
        names.sort()
        day = tools.get_day()
        if not os.path.exists('outfiles/{}'.format(day)):
            os.mkdir('outfiles/{}'.format(day))
        self.names = names
        if len(self.names) > 0:
            self.load_image(0)
        else:
            self.next_btn.Disable()
            self.prev_btn.Disable()
            self.load_blank()

    def on_discard(self, event_):
        name = self.names[self.index]
        day = tools.get_day()
        if not os.path.exists('discard/{}'.format(day)):
            os.mkdir('discard/{}'.format(day))
        os.rename('infiles/' + name, 'discard/{}/{}'.format(day, name))
        self.load_next_image()

    def SetStatusText(self, message):
        self.Parent.Parent.Parent.SetStatusText(message)

    def validate(self):
        return self.static_image.validate_image() \
            and self.validate_group_name()

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
