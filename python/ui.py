#!/usr/bin/env python2
import wx
import wx.lib.imagebrowser
from ui.group_panel import GroupPanel
from ui.calendar_panel import CalendarPanel
from ui.reprint_panel import ReprintPanel

class MainWindow(wx.Frame):
    infile = None

    """ Main Window Frame for Sleigh Photos. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(610, 550))
        self.SetMinSize(self.GetSize())
        self.create_frames()
        self.CreateStatusBar()
        self.setup_menu()
        self.Show(True)

    def create_frames(self):
        self.notebook = wx.Notebook(self)
        self.group_page = wx.NotebookPage(self.notebook)
        self.group_panel = GroupPanel(self.group_page)
        self.notebook.AddPage(self.group_page, "Group")
        self.calendar_page = wx.NotebookPage(self.notebook)
        self.calendar_panel = CalendarPanel(self.calendar_page)
        self.notebook.AddPage(self.calendar_page, "Calendar")
        self.reprint_page = wx.NotebookPage(self.notebook)
        self.reprint_panel = ReprintPanel(self.reprint_page)
        self.notebook.AddPage(self.reprint_page, "Reprint")

    def setup_menu(self):
        """ Setup menu bar. """
        file_menu = wx.Menu()
        menu_open = file_menu.Append(wx.ID_OPEN, "&Open", "Open Photo")
        file_menu.AppendSeparator()
        menu_exit = file_menu.Append(wx.ID_EXIT, "E&xit", "Quit Sleigh Photos")

        help_menu = wx.Menu()
        menu_about = help_menu.Append(wx.ID_ABOUT, "&About",
                                      "About Sleigh Photos")

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_open, menu_open)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)

    def on_about(self, event_):
        about = wx.MessageDialog(
            self,
            "Print photos of Scouts in the sleigh at the Christmas Experience",
            "About Sleigh Photos",
            wx.OK
        )
        about.ShowModal()
        about.Destroy()

    def on_exit(self, event_):
        self.Close(True)

    def on_open(self, event):
        page = self.notebook.GetCurrentPage()
        panel = page.GetChildren()[0]
        panel.OnOpen(event)

    def on_device_added(self, device_id_, properties):
        message = properties.join('\n')
        info = wx.MessageDialog(self, message, "Device Added", wx.OK)
        info.ShowModal()
        info.Destroy()

    def on_device_removed(self, device_id):
        message = "Device Removed: %s" % device_id
        info = wx.MessageDialog(self, message, "Device Removed", wx.OK)
        info.ShowModal()
        info.Destroy()

def main():
    app = wx.App(False)
    MainWindow(None, "Sleigh Photos")
    app.MainLoop()

if __name__ == '__main__':
    main()
