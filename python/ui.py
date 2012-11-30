#!/usr/bin/env python2
import wx
import wx.lib.imagebrowser
import time
import os
import devices
from devices.device import Device
from ui.process_panel import ProcessPanel

class MainWindow(wx.Frame):
    infile = None

    """ Main Window Frame for Sleigh Photos. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(610, 530))
        self.SetMinSize(self.GetSize())
        self.CreateFrames()
        self.CreateStatusBar()
        self.setupMenu()
        self.Show(True)

    def CreateFrames(self):
        self.notebook = wx.Notebook(self)
        self.processPage = wx.NotebookPage(self.notebook)
        self.processPanel = ProcessPanel(self.processPage)
        self.notebook.AddPage(self.processPage, "Process")

    def setupMenu(self):
        """ Setup menu bar. """
        fileMenu = wx.Menu()
        menuOpen = fileMenu.Append(wx.ID_OPEN, "&Open", "Open Photo")
        fileMenu.AppendSeparator()
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
            self.processPanel.staticImage.LoadFromFile(dlg.GetFile())
        dlg.Destroy()

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

def main():
    app = wx.App(False)
    frame = MainWindow(None, "Sleigh Photos")
    app.MainLoop()

if __name__ == '__main__':
    main()
