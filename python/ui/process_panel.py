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
        self.runBtn = wx.Button(self, label="Run")

        self.prevBtn = wx.Button(self, label="<")
        self.prevBtn.Disable()
        self.staticImage = Photo(self)
        self.nextBtn = wx.Button(self, label=">")
        self.nextBtn.Disable()

        self.groupLabel = wx.StaticText(self, label="Group Name:")
        self.groupName = wx.TextCtrl(self)
        self.processBtn = wx.Button(self, label="Process")

        self.Bind(wx.EVT_BUTTON, self.OnRun, self.runBtn)
        self.Bind(wx.EVT_BUTTON, self.OnPrevious, self.prevBtn)
        self.Bind(wx.EVT_BUTTON, self.OnNext, self.nextBtn)
        self.Bind(wx.EVT_BUTTON, self.OnProcess, self.processBtn)

        topRow.Add(self.prevBtn, 1)
        topRow.Add(self.runBtn, 2)
        topRow.Add(self.nextBtn, 1)
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
        if index >= len(self.names) - 1:
            self.nextBtn.Disable()
        else:
            self.nextBtn.Enable()
        if index == 0:
            self.prevBtn.Disable()
        else:
            self.prevBtn.Enable()

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

    def OnRun(self, event):
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
            self.staticImage.LoadBlank()

    def SetStatusText(self, message):
        self.Parent.Parent.Parent.SetStatusText(message)

    def ValidateGroupName(self):
        name = self.groupName.GetValue()
        valid = name != ''
        if not valid:
            wx.MessageBox("Please enter group name",
                          caption="Group name is missing")
        return valid

