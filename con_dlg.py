import configparser 

import wx

from evt_hndler import EventThread


class ConnectingDialog(wx.Dialog):
    def __init__(self, pyttcl):
        wx.Dialog.__init__(self, pyttcl.GUI.Frame, -1, _('Connecting'))
        self.Pyttcl = pyttcl
        self.get_servers_list = lambda: [i.split('"')[1] for i in self.Pyttcl.Config.get('data', 'servers_list').split(', ')]
        self.servers_list = wx.ListBox(self, -1, choices=self.get_servers_list(), pos=(0,0))
        self.servers_list.Bind(wx.EVT_LISTBOX, self.UpdateServerInfoPanel)
        self.serverInfoPanel = wx.Panel(self, -1)
        self.hostnameCtrl = wx.TextCtrl(self.serverInfoPanel, -1)
        self.tcpportCtrl = wx.TextCtrl(self.serverInfoPanel, -1, '10333')
        self.udpportCtrl = wx.TextCtrl(self.serverInfoPanel, -1, '10333')
        self.UsernameCtrl = wx.TextCtrl(self.serverInfoPanel, -1)
        self.PasswordCtrl = wx.TextCtrl(self.serverInfoPanel, -1, style=wx.TE_PASSWORD)
        self.ChannelCtrl = wx.TextCtrl(self.serverInfoPanel, -1)
        self.ChannelPasswordCtrl = wx.TextCtrl(self.serverInfoPanel, -1, style=wx.TE_PASSWORD)
        self.NoteName = wx.TextCtrl(self.serverInfoPanel, -1)
        self.servers_list.Select(0)
        self.UpdateServerInfoPanel()
        RemoveButton = wx.Button(self, -1, _('Remove'))
        RemoveButton.Bind(wx.EVT_BUTTON, self.Remove)
        SaveButton = wx.Button(self, -1, _('Save'))
        SaveButton.Bind(wx.EVT_BUTTON, self.Save)
        connect_button = wx.Button(self, -1, _('Connect'))
        connect_button.Bind(wx.EVT_BUTTON, self.connect)
        self.Bind(
            wx.EVT_CHAR_HOOK,
            lambda evt: self.Destroy() if evt.GetKeyCode() == wx.WXK_ESCAPE else evt.Skip()
        )
        self.Show()

    def connect(self, evt=None):
        if self.hostnameCtrl.GetValue() != '' and (self.tcpportCtrl.GetValue().isdigit() and int(self.tcpportCtrl.GetValue()) > 0 and int(self.tcpportCtrl.GetValue()) < 65536) and (self.udpportCtrl.GetValue().isdigit()   and int(self.udpportCtrl.GetValue()) > 0 and int(self.udpportCtrl.GetValue()) < 65536):
            self.Destroy()
        else:
            wx.MessageBox(_('Please fill in the following required fields:\nhost\ntcp port (integer in the range from 1 to 6535)\nudp port (integer in the range from 1 to 65535)'), _('Error'))
            return
        self.Pyttcl.EventThread = EventThread(self.Pyttcl)
        self    .Pyttcl.EventThread.setDaemon(True)
        self.Pyttcl.EventThread.start()
        self.Pyttcl.TeamTalk.connect(
            self.hostnameCtrl.GetValue(),
            int(self.tcpportCtrl.GetValue()),
            int(self.udpportCtrl.GetValue())
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

    def Remove(self, evt=None):
        self.Pyttcl.Config.remove_section(self.get_servers_list()[self.servers_list.GetSelection()])
        servers_list = self.get_servers_list()
        servers_list.pop(self.servers_list.GetSelection())
        self.Pyttcl.Config['data']['servers_list'] = ', '.join([f'"{i }"' for i in servers_list])
        with open(self.Pyttcl.ConfigFile, 'w', encoding='UTF-8') as f:
            self.Pyttcl.Config.write(f)
        self.updateServersList()

    def Save(self, evt=None):
        newSection = configparser.SectionProxy(self.Pyttcl.Config, self.NoteName.GetValue())
        self.Pyttcl.Config[self.NoteName.GetValue()] = newSection
        newSection['host'] = self.hostnameCtrl.GetValue()
        newSection['tcpport'] = self.tcpportCtrl.GetValue()
        newSection['udpport'] = self.udpportCtrl.GetValue()
        newSection['username'] = self.UsernameCtrl.GetValue()
        newSection['password'] = self.PasswordCtrl.GetValue()
        newSection['channel']  = self.ChannelCtrl.GetValue()
        newSection['channel_password'] = self.ChannelPasswordCtrl.GetValue()
        if self.NoteName.GetValue() not in self.get_servers_list():
            self.Pyttcl.Config['data']['servers_list'] += f', "{self.NoteName.GetValue()}"'
        with open(self.Pyttcl.ConfigFile, 'w', encoding='UTF-8') as f:
            self.Pyttcl.Config.write(f)
        self.updateServersList()

    def UpdateServerInfoPanel(self, evt=None):
        server_data = self.Pyttcl.Config[self.get_servers_list()[self.servers_list.GetSelection()]]
        self.hostnameCtrl.SetValue(server_data['host'])
        self.tcpportCtrl.SetValue(server_data['tcpport'])
        self.udpportCtrl.SetValue(server_data['udpport'])
        self.UsernameCtrl.SetValue(server_data['username'])
        self.PasswordCtrl.SetValue(server_data['password'])
        self.ChannelCtrl.SetValue(server_data['channel'])
        self.ChannelPasswordCtrl.SetValue(server_data['channel_password'])
        self.NoteName.SetValue(server_data.name)

    def updateServersList(self):
        self.servers_list.Destroy()
        self.servers_list = wx.ListBox(self, -1, choices=self.get_servers_list(), pos=(0,0))
        self.servers_list.Select(0)
        self.UpdateServerInfoPanel()
