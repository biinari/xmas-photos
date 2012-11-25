#!/usr/bin/env python2
import wx
import wx.lib.imagebrowser
import os
import devices
from devices.device import Device

class MainWindow(wx.Frame):
    """ Main Window Frame for Sleigh Photos. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.createWidgets()
        self.CreateStatusBar()
        self.setupMenu()
        self.Show(True)

    def createWidgets(self):
        vert = wx.BoxSizer(wx.VERTICAL)
        horiz = wx.BoxSizer(wx.HORIZONTAL)
        self.staticImage = wx.StaticBitmap(self, wx.ID_ANY)
        self.staticImage.SetSize((600, 400))
        self.scheduleCtrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.processBtn = wx.Button(self, label="Process")

        self.Bind(wx.EVT_BUTTON, self.OnProcess, self.processBtn)

        horiz.Add(self.processBtn, 1, wx.ALIGN_LEFT)
        horiz.Add(self.scheduleCtrl, 1, wx.EXPAND)
        vert.Add(horiz)
        self.SetSizer(vert)
        self.Centre()

    def setupMenu(self):
        """ Setup menu bar. """
        fileMenu = wx.Menu()
        menuOpen = fileMenu.Append(wx.ID_OPEN, "&Open", "Open Photo")
        menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit", "Quit Sleigh Photos")

        helpMenu = wx.Menu()
        menuAbout = helpMenu.Append(wx.ID_ABOUT, "&About",
                                    "About Sleigh Photos")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
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

    def OnOpen(self, event):
        cwd = os.getcwd()
        initial_dir = os.path.join(cwd, 'png')
        dlg = wx.lib.imagebrowser.ImageDialog(self, initial_dir)
        dlg.Centre()
        if dlg.ShowModal() == wx.ID_OK:
            self.LoadImage(dlg.GetFile())
        dlg.Destroy()

    def LoadImage(self, name):
        image = wx.Image(name)
        (width, height) = self.staticImage.GetSize()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.BitmapFromImage(image)
        self.staticImage.SetBitmap(bitmap)

    def OnProcess(self, event):
        process.process()

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
