import webbrowser

import wx

from con_dlg import ConnectingDialog

from inf_dlg import InfoDialog

from msg_dlg import MessageDialog


class GUI(wx.App):
    def __init__(self, pyttcl):
        wx.App.__init__(self)
        self.Pyttcl = pyttcl
        self.Frame = Frame(self.Pyttcl)


class Frame(wx.Frame):
    def __init__(self, pyttcl):
        wx.Frame.__init__(self, None, -1, 'pyttcl')
        self.Pyttcl = pyttcl
        self.SetMenuBar(MenuBar(pyttcl))
        self.CreateStatusBar()
        self.Tree = wx.TreeCtrl(self)
        self.Show()


class MenuBar(wx.MenuBar):
    def __init__(self, pyttcl):
        wx.MenuBar.__init__(self)
        self.Pyttcl = pyttcl
        ClientMenu = wx.Menu()
        ConnectItem = ClientMenu.Append(
            -1, _('Connect\t{hotkey}').format(
                hotkey=self.Pyttcl.Config.get('hotkey', 'connect')
            )
        )
        ClientMenu.Bind(
            wx.EVT_MENU, lambda evt: ConnectingDialog(self.Pyttcl), ConnectItem
        )
        DisconnectItem = ClientMenu.Append(
            -1, _('Disconnect\t{hotkey}').format(
                hotkey=self.Pyttcl.Config.get('hotkey', 'disconnect')
            )
        )
        ClientMenu.Bind(wx.EVT_MENU, self.Disconnect, DisconnectItem)
        DisconnectItem.Enable(False)
        self.Append(ClientMenu, _('Client'))
        ChannelMenu = wx.Menu()
        Get_channel_infoItem = ChannelMenu.Append(
            -1, _('Get channel info\t{hotkey}').format(
                hotkey=self.Pyttcl.Config.get('hotkey', 'get_channel_info')
            )
        )
        ChannelMenu.Bind(
            wx.EVT_MENU, lambda evt: InfoDialog(self.Pyttcl),
            Get_channel_infoItem
        )
        self.Append(ChannelMenu, _('Channel'))
        UserMenu = wx.Menu()
        Get_user_infoItem = UserMenu.Append(
            -1, _('Get user info\t{hotkey}').format(
                hotkey=self.Pyttcl.Config.get('hotkey', 'get_user_info')
            )
        )
        UserMenu.Bind(
            wx.EVT_MENU, lambda evt: InfoDialog(self.Pyttcl),
            Get_user_infoItem
        )
        user_message = UserMenu.Append(
            -1, _('User Message\t{hotkey}').format(
                hotkey=self.Pyttcl.Config.get('hotkey', 'user_msg')
            )
        )
        UserMenu.Bind(
            wx.EVT_MENU, lambda evt: MessageDialog(self.Pyttcl, self.Pyttcl.MainTreeviewData[self.Pyttcl.GUI.Frame.Tree.GetSelection()]), user_message
        )
        self.Append(UserMenu, _('User'))
        HelpMenu = wx.Menu()
        GetHelpItem = HelpMenu.Append(
            -1, _('Get help\t{hotkey}').format(
                hotkey=self.Pyttcl.Config.get('hotkey', 'get_help')
            )
        )
        HelpMenu.Bind(
            wx.EVT_MENU,
            lambda evt: webbrowser.open(f"https://gumerov-amir.github.io/Pyttcl/{self.Pyttcl.Config.get('settings', 'language')}"),
            GetHelpItem
        )
        self.Append(HelpMenu, _('Help'))

    def Disconnect(self, evt):
        self.Pyttcl.GUI.Frame.GetMenuBar().GetMenu(0).GetMenuItems()[0].Enable(
            True
        )
        self.Pyttcl.GUI.Frame.GetMenuBar().GetMenu(0).GetMenuItems()[1].Enable(
            False
        )
        self.Pyttcl.TeamTalk.disconnect()
        self.Pyttcl.GUI.Frame.Tree.Destroy()
        del self.Pyttcl.GUI.Frame.Tree
        self.Pyttcl.GUI.Frame.Tree = wx.TreeCtrl(self.Pyttcl.GUI.Frame)
        del self.Pyttcl.MainTreeviewData
        self.Pyttcl.MainTreeviewData = {}
        self.Pyttcl.is_connected = None
        self.Pyttcl.is_loggedin = None
        del self.Pyttcl.EventThread
