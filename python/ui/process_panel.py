import wx
import os
import shutil
import time
from ui.photo import Photo
import process
import tools

class ProcessPanel(wx.Panel):

    """ Files in infiles/ for choosing from (just the basenames) """
    names = []
    """ Current index into self.names """
    index = 0

    """ Panel to select and process photo """
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.CreateWidgets()

    def CreateWidgets(self):
        vert = wx.BoxSizer(wx.VERTICAL)
        topRow = wx.BoxSizer(wx.HORIZONTAL)
        horiz = wx.BoxSizer(wx.HORIZONTAL)
        self.getPhotosBtn = wx.Button(self, label="Get Photos")
        self.discardBtn = wx.Button(self, label="Discard")
        self.discardBtn.Disable()

        self.prevBtn = wx.Button(self, label="<")
        self.prevBtn.Disable()
        self.staticImage = Photo(self)
        self.nextBtn = wx.Button(self, label=">")
        self.nextBtn.Disable()

        self.groupLabel = wx.StaticText(self, label="Group Name:")
        self.groupName = wx.TextCtrl(self)
        self.processBtn = wx.Button(self, label="Process")

        self.Bind(wx.EVT_BUTTON, self.OnGetPhotos, self.getPhotosBtn)
        self.Bind(wx.EVT_BUTTON, self.OnDiscard, self.discardBtn)
        self.Bind(wx.EVT_BUTTON, self.OnPrevious, self.prevBtn)
        self.Bind(wx.EVT_BUTTON, self.OnNext, self.nextBtn)
        self.Bind(wx.EVT_BUTTON, self.OnProcess, self.processBtn)

        topRow.Add(self.prevBtn, 1)
        topRow.Add(self.getPhotosBtn, 2)
        topRow.Add(self.nextBtn, 1)
        topRow.Add(self.discardBtn, 2)
        horiz.Add(self.groupLabel, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        horiz.Add(self.groupName, 4, wx.ALIGN_CENTER_VERTICAL)
        horiz.Add(self.processBtn, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        vert.Add(topRow, 1, wx.ALIGN_CENTER_HORIZONTAL)
        vert.Add(self.staticImage, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 5)
        vert.Add(horiz, 1, wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(vert)
        self.Centre()

    def LoadImage(self, index):
        self.index = index
        self.staticImage.LoadFromFile('infiles/' + self.names[index])
        self.discardBtn.Enable()
        if index >= len(self.names) - 1:
            self.nextBtn.Disable()
        else:
            self.nextBtn.Enable()
        if index == 0:
            self.prevBtn.Disable()
        else:
            self.prevBtn.Enable()

    def LoadNextImage(self):
        del(self.names[self.index])
        if len(self.names) > self.index:
            self.LoadImage(self.index)
        elif len(self.names) > 0:
            self.LoadImage(len(self.names) - 1)
        else:
            self.LoadBlank()

    def LoadBlank(self):
        self.staticImage.LoadBlank()
        self.discardBtn.Disable()

    def OnNext(self, event):
        if self.index + 1 < len(self.names):
            self.LoadImage(self.index + 1)

    def OnPrevious(self, event):
        if self.index > 0:
            self.LoadImage(self.index - 1)

    def OnOpen(self, event):
        cwd = os.getcwd()
        initial_dir = os.path.join(cwd)
        dlg = wx.lib.imagebrowser.ImageDialog(self, initial_dir)
        dlg.Centre()
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetFile()
            name = os.path.basename(path)
            shutil.copyfile(path, 'infiles/' + name)
            self.names.append(name)
            self.LoadImage(len(self.names) - 1)
        dlg.Destroy()

    def OnProcess(self, event):
        if self.staticImage.ValidateImage() and self.ValidateGroupName():
            timeid = time.strftime('%a/%H%M%S', time.localtime())
            infile = self.names[self.index]
            group_name = self.groupName.GetValue()
            process.process(infile, group_name, timeid)
            os.rename('infiles/' + infile, 'outfiles/{}_{}.jpg'.format(timeid, group_name.replace(' ','_')))
            self.LoadNextImage()

    def OnGetPhotos(self, event):
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
            self.LoadImage(0)
        else:
            self.nextBtn.Disable()
            self.prevBtn.Disable()
            self.LoadBlank()

    def OnDiscard(self, event):
        name = self.names[self.index]
        day = tools.get_day()
        if not os.path.exists('discard/{}'.format(day)):
            os.mkdir('discard/{}'.format(day))
        os.rename('infiles/' + name, 'discard/{}/{}'.format(day, name))
        self.LoadNextImage()

    def SetStatusText(self, message):
        self.Parent.Parent.Parent.SetStatusText(message)

    def ValidateGroupName(self):
        name = self.groupName.GetValue()
        valid = name != ''
        if not valid:
            wx.MessageBox("Please enter group name",
                          caption="Group name is missing")
        return valid

