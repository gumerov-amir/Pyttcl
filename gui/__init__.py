import webbrowser


import wx

from .con_dlg import ConnectingDialog

from .inf_dlg import InfoDialog

from .msg_dlg import MessageDialog

from lib.TeamTalk5 import Channel


class GUI(wx.App):
    def __init__(self, pyttcl):
        wx.App.__init__(self)
        self.pyttcl = pyttcl
        self.frame = Frame(self.pyttcl)
        self.frame_height = self.frame.GetSize().GetHeight()
        self.frame_width = self.frame.GetSize().GetWidth()


class Frame(wx.Frame):
    def __init__(self, pyttcl):
        wx.Frame.__init__(self, None, -1, 'pyttcl')
        self.pyttcl = pyttcl
        self.SetMenuBar(MenuBar(pyttcl))
        self.CreateStatusBar()
        self.tree = wx.TreeCtrl(self)
        self.Show()


class MenuBar(wx.MenuBar):
    def __init__(self, pyttcl):
        wx.MenuBar.__init__(self)
        self.pyttcl = pyttcl
        client_menu = wx.Menu()
        connect_item = client_menu.Append(
            -1, _('Connect\t{hotkey}').format(
                hotkey=self.pyttcl.Config.get('hotkey', 'connect')
            )
        )
        client_menu.Bind(
            wx.EVT_MENU, lambda evt: ConnectingDialog(self.pyttcl), connect_item
        )
        disconnect_item = client_menu.Append(
            -1, _('Disconnect\t{hotkey}').format(
                hotkey=self.pyttcl.Config.get('hotkey', 'disconnect')
            )
        )
        client_menu.Bind(wx.EVT_MENU, self.Disconnect, disconnect_item)
        disconnect_item.Enable(False)
        self.Append(client_menu, _('Client'))
        ChannelMenu = wx.Menu()
        Get_channel_infoItem = ChannelMenu.Append(
            -1, _('Get channel info\t{hotkey}').format(
                hotkey=self.pyttcl.Config.get('hotkey', 'get_channel_info')
            )
        )
        ChannelMenu.Bind(
            wx.EVT_MENU, lambda evt: InfoDialog(self.pyttcl),
            Get_channel_infoItem
        )
        ConnectChannelItem = ChannelMenu.Append(
            -1, _('Connect\t{hotkey}').format(
                hotkey=self.pyttcl.Config['hotkey']['connect_to_channel']
            )
        )
        ChannelMenu.Bind(
            wx.EVT_MENU, lambda evt: self.ConnectToChannel(), ConnectChannelItem
        )
        channel_message = ChannelMenu.Append(
            -1, _('Channel Message\t{hotkey}').format(
                hotkey=self.pyttcl.Config.get('hotkey', 'channel_msg')
            )
        )
        ChannelMenu.Bind(
            wx.EVT_MENU, lambda evt: MessageDialog(self.pyttcl, self.pyttcl.MainTreeviewData[self.pyttcl.gui.frame.tree.GetSelection()]), channel_message
        )
        self.Append(ChannelMenu, _('Channel'))
        UserMenu = wx.Menu()
        Get_user_infoItem = UserMenu.Append(
            -1, _('Get user info\t{hotkey}').format(
                hotkey=self.pyttcl.Config.get('hotkey', 'get_user_info')
            )
        )
        UserMenu.Bind(
            wx.EVT_MENU, lambda evt: InfoDialog(self.pyttcl),
            Get_user_infoItem
        )
        user_message = UserMenu.Append(
            -1, _('User Message\t{hotkey}').format(
                hotkey=self.pyttcl.Config.get('hotkey', 'user_msg')
            )
        )
        UserMenu.Bind(
            wx.EVT_MENU, lambda evt: MessageDialog(self.pyttcl, self.pyttcl.MainTreeviewData[self.pyttcl.gui.frame.tree.GetSelection()]), user_message
        )
        self.Append(UserMenu, _('User'))
        OptionMenu = wx.Menu()
        change_nickname = OptionMenu.Append(-1, _('Change nickname\t{hotkey}').format(
            hotkey=self.pyttcl.Config.get('hotkey', 'change_nickname')
        ))
        OptionMenu.Bind(wx.EVT_MENU, self.ChangeNickname, change_nickname)
        en_dis_voice_act = OptionMenu.Append(-1, _('Enable or disable voice activation\t{hotkey}').format(
            hotkey=self.pyttcl.Config.get('hotkey', 'voice_activation')
        ))
        OptionMenu.Bind(wx.EVT_MENU, self.enable_disable_voice_activation)
        self.Append(OptionMenu, _('Options'))
        HelpMenu = wx.Menu()
        GetHelpItem = HelpMenu.Append(
            -1, _('Get help\t{hotkey}').format(
                hotkey=self.pyttcl.Config.get('hotkey', 'get_help')
            )
        )
        HelpMenu.Bind(
            wx.EVT_MENU,
            lambda evt: webbrowser.open(f"https://gumerov-amir.github.io/pyttcl/{self.pyttcl.Config.get('settings', 'language')}"),
            GetHelpItem
        )
        self.Append(HelpMenu, _('Help'))

    def ChangeNickname(self, evt=None):
        dialog = wx.TextEntryDialog(self.pyttcl.gui.frame, _('enter you new nickname'), _('Changing nickname'))
        if dialog.ShowModal() == wx.ID_OK:
            self.pyttcl.TeamTalk.doChangeNickname(dialog.GetValue())


    def ConnectToChannel(self):
        if type(self.pyttcl.MainTreeviewData[self.pyttcl.gui.frame.tree.GetSelection()]) == Channel:
            self.pyttcl.TeamTalk.doJoinChannelByID(self.pyttcl.MainTreeviewData[self.pyttcl.gui.frame.tree.GetSelection()].nChannelID, '')

    def Disconnect(self, evt):
        self.pyttcl.gui.frame.GetMenuBar().GetMenu(0).GetMenuItems()[0].Enable(True)
        self.pyttcl.gui.frame.GetMenuBar().GetMenu(0).GetMenuItems()[1].Enable(False)
        self.pyttcl.TeamTalk.disconnect()
        self.pyttcl.gui.frame.tree.Destroy()
        del self.pyttcl.gui.frame.tree
        self.pyttcl.gui.frame.tree = wx.TreeCtrl(self.pyttcl.gui.frame)
        del self.pyttcl.MainTreeviewData
        self.pyttcl.MainTreeviewData = {}
        self.pyttcl.is_connected = None
        self.pyttcl.is_loggedin = None
        del self.pyttcl.event_thread

    def enable_disable_voice_activation(self, evt=None):
        self.pyttcl.TeamTalk.enableVoiceTransmission(not self.pyttcl.is_enable_voice_activation)
        self.pyttcl.is_enable_voice_activation = not self.pyttcl.is_enable_voice_activation
