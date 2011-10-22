#!/usr/bin/env python
import wx
import devices

class MainWindow(wx.Frame):
    """ Main Window Frame for Sleigh Photos. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.scheduleCtrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()
        self.setupMenu()
        self.Show(True)

    def setupMenu(self):
        """ Setup menu bar. """
        fileMenu = wx.Menu()
        menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit", "Quit Sleigh Photos")

        helpMenu = wx.Menu()
        menuAbout = helpMenu.Append(wx.ID_ABOUT, "&About",
                                    "About Sleigh Photos")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

    def OnAbout(self, event):
        about = wx.MessageDialog(
            self,
            "Print photos of Scouts in the sleigh at the Christmas Experience",
            "About Sleigh Photos",
            wx.OK
        )
        about.ShowModal()
        about.Destroy()

    def OnExit(self, event):
        self.Close(True)

    def OnDeviceAdded(self, device_id, properties):
        message = properties.join('\n')
        info = wx.MessageDialog(self, message, "Device Added", wx.OK)
        info.ShowModal()
        info.Destroy()

    def OnDeviceRemoved(self, device_id):
        message = "Device Removed: %s" % device_id
        info = wx.MessageDialog(self, message, "Device Removed", wx.OK)
        info.ShowModal()
        info.Destroy()

app = wx.App(False)
frame = MainWindow(None, "Sleigh Photos")
app.MainLoop()
