import wx

from evt_hndler import EventThread


class ConnectingDialog(wx.Dialog):
    def __init__(self, pyttcl):
        wx.Dialog.__init__(self, pyttcl.GUI.Frame, -1, _('Connecting'))
        self.Pyttcl = pyttcl
        self.servers_list = wx.ListBox(
            self, -1,
            choices=[i.split('"')[1] for i in self.Pyttcl.Config.get(
                'data', 'servers_list'
            ).split(', ')]
        )
        self.servers_list.Bind(wx.EVT_LISTBOX, self.UpdateServerInfoPanel)
        self.serverInfoPanel = wx.Panel(self, -1)
        self.hostnameCtrl = wx.TextCtrl(self.serverInfoPanel, -1)
        self.tcpportCtrl = wx.TextCtrl(self.serverInfoPanel, -1, '10333')
        self.udpportCtrl = wx.TextCtrl(self.serverInfoPanel, -1, '10333')
        self.UsernameCtrl = wx.TextCtrl(self, -1)
        self.PasswordCtrl = wx.TextCtrl(self, -1, style=wx.TE_PASSWORD)
        self.ChannelCtrl = wx.TextCtrl(self, -1)
        self.ChannelPasswordCtrl = wx.TextCtrl(self, -1, style=wx.TE_PASSWORD)
        self.servers_list.Select(0)
        self.UpdateServerInfoPanel()
        connect_button = wx.Button(self, -1, _('Connect'))
        connect_button.Bind(wx.EVT_BUTTON, self.connect)
        self.Bind(
            wx.EVT_CHAR_HOOK,
            lambda evt: self.Destroy() if evt.GetKeyCode() == wx.WXK_ESCAPE else evt.Skip()
        )
        self.Show()

    def connect(self, evt=None):
        self.Destroy()
        self.Pyttcl.EventThread = EventThread(self.Pyttcl)
        self.Pyttcl.EventThread.setDaemon(True)
        self.Pyttcl.EventThread.start()
        self.Pyttcl.TeamTalk.connect(
            self.hostnameCtrl.GetValue(),
            self.tcpportCtrl.GetValue(),
            self.udpportCtrl.GetValue()
        )
        while self.Pyttcl.is_connected is not True:
            if self.Pyttcl.is_connected is False:
                wx.MessageBox(_('Not connected'), _('Error'))
                return
            else:
                pass
        self.Pyttcl.TeamTalk.doLogin(
            self.Pyttcl.Config.get('settings', 'nickname'),
            self.UsernameCtrl.GetValue(), self.PasswordCtrl.GetValue(),
            'pyttcl'
        )
        while self.Pyttcl.is_loggedin is None:
            pass
        #self.Pyttcl.TeamTalk.doJoinChannelByID(
         #   int(server_data['channel_id']), server_data['channel_password']
        #)
        self.Pyttcl.GUI.Frame.GetMenuBar().GetMenu(0).GetMenuItems()[0].Enable(False)
        self.Pyttcl.GUI.Frame.GetMenuBar().GetMenu(0).GetMenuItems()[1].Enable(True)

    def UpdateServerInfoPanel(self, evt=None):
        server_data = dict(
            self.Pyttcl.Config[
                self.Pyttcl.Config.get(
                    'data', 'servers_list'
                ).split(', ')[self.servers_list.GetSelection()].split('"')[1]
            ]
        )
        self.hostnameCtrl.SetValue(server_data['host'])
        self.tcpportCtrl.SetValue(int(server_data['tcpport']))
        self.udpportCtrl.SetValue(int(server_data['udpport']))
        self.UsernameCtrl.SetValue(server_data['username'])
        self.PasswordCtrl.SetValue(server_data['password'])
        self.ChannelCtrl.SetValue(server_data['channel'])
        self.ChannelPasswordCtrl.SetValue(server_data['channel_password'])
