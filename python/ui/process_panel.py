import wx
from ui.photo import Photo
import process
import tools

class ProcessPanel(wx.Panel):

    """ Panel to select and process photo """
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.CreateWidgets()

    def CreateWidgets(self):
        vert = wx.BoxSizer(wx.VERTICAL)
        horiz = wx.BoxSizer(wx.HORIZONTAL)
        self.staticImage = Photo(self)
        self.groupLabel = wx.StaticText(self, label="Group Name:")
        self.groupName = wx.TextCtrl(self)
        self.processBtn = wx.Button(self, label="Process")

        self.Bind(wx.EVT_BUTTON, self.OnProcess, self.processBtn)

        horiz.Add(self.groupLabel, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        horiz.Add(self.groupName, 4, wx.ALIGN_CENTER_VERTICAL)
        horiz.Add(self.processBtn, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
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

    def OnProcess(self, event):
        if self.staticImage.ValidateImage() and self.ValidateGroupName():
            timeid = time.strftime('%a/%H%M%S', time.localtime())
            process.process(self.infile, self.groupName.GetValue(), timeid)

    def ValidateGroupName(self):
        name = self.groupName.GetValue()
        if name == '':
            wx.MessageBox("Please enter group name",
                          caption="Group name is missing")
        return name != ''

