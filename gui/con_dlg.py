# -*- coding: UTF-8 -*-

"""Config dialog."""

import configparser

import wx

from .evt_hndler import EventThread


class ConnectingDialog(wx.Dialog):
    """Class defines connecting dialog."""

    def __init__(self, pyttcl):
        """Initialize."""
        wx.Dialog.__init__(self, pyttcl.gui.frame, -1, _('Connecting'))
        self.pyttcl = pyttcl
        self.get_servers_list = lambda: [
            i.split('"')[1] for i in self.pyttcl.Config.get(
                'data', 'servers_list'
            ).split(', ')
        ]
        wx.StaticText(
            self, -1, _('Servers list'), pos=(0, 0), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 30
            )
        )
        self.servers_listbox = wx.ListBox(
            self, -1, choices=self.get_servers_list(), pos=(0, 50), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 200
            )
        )
        self.servers_listbox.Bind(
            wx.EVT_LISTBOX, self.update_server_info_panel
        )
        wx.StaticText(
            self, -1, _('Server information'), pos=(
                int(self.pyttcl.gui.frame_width * 0.384), 0
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 30
            )
        )
        self.server_info_panel = wx.Panel(
            self, -1, pos=(
                int(self.pyttcl.gui.frame_width * 0.0769), 70
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.6152), 100
            )
        )
        wx.StaticText(
            self.server_info_panel, -1, _('Host name'), pos=(0, 0), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 30
            )
        )
        self.hostname_textctrl = wx.TextCtrl(
            self.server_info_panel, -1, pos=(0, 50), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 50
            )
        )
        wx.StaticText(
            self.server_info_panel, -1, _('TCP port'), pos=(
                int(self.pyttcl.gui.frame_width * 0.0769), 0
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 30
            )
        )
        self.tcpport_textctrl = wx.TextCtrl(
            self.server_info_panel, -1, '10333', pos=(
                int(self.pyttcl.gui.frame_width * 0.0769), 50
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 50
            )
        )
        wx.StaticText(
            self.server_info_panel, -1, _('UDP port'), pos=(
                int(self.pyttcl.gui.frame_width * 0.154), 0
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 30
            )
        )
        self.udpport_textctrl = wx.TextCtrl(
            self.server_info_panel, -1, '10333', pos=(
                int(self.pyttcl.gui.frame_width * 0.154), 50
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 50
            )
        )
        wx.StaticText(
            self.server_info_panel, -1, _('User name'), pos=(
                int(self.pyttcl.gui.frame_width * 0.231), 0
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 30
            )
        )
        self.username_textctrl = wx.TextCtrl(
            self.server_info_panel, -1, pos=(
                int(self.pyttcl.gui.frame_width * 0.231), 50
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 50
            )
        )
        wx.StaticText(
            self.server_info_panel, -1, _('Password'), pos=(
                int(self.pyttcl.gui.frame_width * 0.307), 0
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 30
            )
        )
        self.password_textctrl = wx.TextCtrl(
            self.server_info_panel, -1, pos=(
                int(self.pyttcl.gui.frame_width * 0.307), 50
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 50
            ), style=wx.TE_PASSWORD
        )
        wx.StaticText(
            self.server_info_panel, -1, _('Channel path'), pos=(
                int(self.pyttcl.gui.frame_width * 0.384), 0
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 30
            )
        )
        self.channel_textctrl = wx.TextCtrl(
            self.server_info_panel, -1, pos=(
                int(self.pyttcl.gui.frame_width * 0.384), 50
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 50
            )
        )
        wx.StaticText(
            self.server_info_panel, -1, _('Channel password'), pos=(
                int(self.pyttcl.gui.frame_width * 0.462), 0
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 30
            )
        )
        self.channel_password_textctrl = wx.TextCtrl(
            self.server_info_panel, -1, pos=(
                int(self.pyttcl.gui.frame_width * 0.462), 50
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 50
            ), style=wx.TE_PASSWORD
        )
        wx.StaticText(
            self.server_info_panel, -1, _('Note name'), pos=(
                int(self.pyttcl.gui.frame_width * 0.538), 0
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 30
            )
        )
        self.note_name_textctrl = wx.TextCtrl(
            self.server_info_panel, -1, pos=(
                int(self.pyttcl.gui.frame_width * 0.538), 50
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 50
            )
        )
        self.servers_listbox.Select(0)
        self.update_server_info_panel()
        remove_button = wx.Button(
            self, -1, _('Remove'), pos=(
                int(self.pyttcl.gui.frame_width * 0.692), 0
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.83), 50
            )
        )
        remove_button.Bind(wx.EVT_BUTTON, self.remove_server)
        save_button = wx.Button(
            self, -1, _('Save'), pos=(
                int(self.pyttcl.gui.frame_width * 0.769), 0
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 50
            )
        )
        save_button.Bind(wx.EVT_BUTTON, self.save_server)
        new_server_button = wx.Button(
            self, -1, _('New server'), pos=(
                int(self.pyttcl.gui.frame_width * 0.846), 0
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 50
            )
        )
        new_server_button.Bind(wx.EVT_BUTTON, self.new_server)
        connect_button = wx.Button(
            self, -1, _('Connect'), pos=(
                int(self.pyttcl.gui.frame_width * 0.923), 0
            ), size=(
                int(self.pyttcl.gui.frame_width * 0.0769), 30
            )
        )
        connect_button.Bind(wx.EVT_BUTTON, self.connect)
        self.Bind(
            wx.EVT_CHAR_HOOK,
            lambda evt: self.Destroy() if evt.GetKeyCode() == wx.WXK_ESCAPE else evt.Skip()
        )
        self.Show()

    def connect(self, evt=None):
        """Connect to ser with parametrs entered in server information panel."""
        if not (self.hostname_textctrl.GetValue() != '' and (self.tcpport_textctrl.GetValue().isdigit() and int(self.tcpport_textctrl.GetValue()) > 0 and int(self.tcpport_textctrl.GetValue()) < 65536) and (self.udpport_textctrl.GetValue().isdigit() and int(self.udpport_textctrl.GetValue()) > 0 and int(self.udpport_textctrl.GetValue()) < 65536)):
            wx.MessageBox(_(
                """Please fill in the following required fields:
host
tcp port (integer in the range from 1 to 65535)
udp port (integer in the range from 1 to 65535)"""
            ), _('Error'))
            return
        self.Destroy()
        self.pyttcl.event_thread = EventThread(self.pyttcl)
        self    .pyttcl.event_thread.setDaemon(True)
        self.pyttcl.event_thread.start()
        self.pyttcl.TeamTalk.connect(
            self.hostname_textctrl.GetValue(),
            int(self.tcpport_textctrl.GetValue()),
            int(self.udpport_textctrl.GetValue())
        )
        while self.pyttcl.is_connected is not True:
            if self.pyttcl.is_connected is False:
                wx.MessageBox(_('Not connected'), _('Error'))
                return
            else:
                pass
        self.pyttcl.TeamTalk.doLogin(
            self.pyttcl.Config.get('settings', 'nickname'),
            self.username_textctrl.GetValue(),
            self.password_textctrl.GetValue(),
            'pyttcl'
        )
        while self.pyttcl.is_loggedin is None:
            pass
        self.pyttcl.gui.frame.GetMenuBar().GetMenu(0).GetMenuItems()[0].Enable(False)
        self.pyttcl.gui.frame.GetMenuBar().GetMenu(0).GetMenuItems()[1].Enable(True)

    def new_server(self, evt=None):
        """Prepare the server_info_panel to creating new server."""
        self.servers_listbox.Deselect(self.servers_listbox.GetSelection())
        self.hostname_textctrl.SetValue('')
        self.tcpport_textctrl.SetValue('10333')
        self.udpport_textctrl.SetValue('10333')
        self.username_textctrl.SetValue('')
        self.password_textctrl.SetValue('')
        self.channel_textctrl.SetValue('')
        self.channel_password_textctrl.SetValue('')
        self.note_name_textctrl.SetValue('')

    def remove_server(self, evt=None):
        """Remove the selected server."""
        self.pyttcl.Config.remove_section(
            self.get_servers_list()[self.servers_listbox.GetSelection()]
        )
        servers_list = self.get_servers_list()
        servers_list.pop(self.servers_listbox.GetSelection())
        self.pyttcl.Config['data']['servers_list'] = ', '.join(
            [f'"{i }"' for i in servers_list]
        )
        with open(self.pyttcl.ConfigFile, 'w', encoding='UTF-8') as f:
            self.pyttcl.Config.write(f)
        self.update_servers_list()

    def save_server(self, evt=None):
        """Save information about server from server information panel."""
        if not (self.hostname_textctrl.GetValue() != '' and (self.tcpport_textctrl.GetValue().isdigit() and int(self.tcpport_textctrl.GetValue()) > 0 and int(self.tcpport_textctrl.GetValue()) < 65536) and (self.udpport_textctrl.GetValue().isdigit() and int(self.udpport_textctrl.GetValue()) > 0 and int(self.udpport_textctrl.GetValue()) < 65536) and self.note_name_textctrl.GetValue() == ''):
            wx.MessageBox(_(
                """Please fill in the following required fields:
host
tcp port (integer in the range from 1 to 65535)
udp port (integer in the range from 1 to 65535)
Note name"""
            ), _('Error'))
            return
        new_section = configparser.SectionProxy(
            self.pyttcl.Config, self.note_name_textctrl.GetValue()
        )
        self.pyttcl.Config[self.note_name_textctrl.GetValue()] = new_section
        new_section['host'] = self.hostname_textctrl.GetValue()
        new_section['tcpport'] = self.tcpport_textctrl.GetValue()
        new_section['udpport'] = self.udpport_textctrl.GetValue()
        new_section['username'] = self.username_textctrl.GetValue()
        new_section['password'] = self.password_textctrl.GetValue()
        new_section['channel'] = self.channel_textctrl.GetValue()
        new_section['channel_password'] = self.channel_password_textctrl.GetValue()
        if self.note_name_textctrl.GetValue() not in self.get_servers_list():
            self.pyttcl.Config['data']['servers_list'] += f""", \"{
                self.note_name_textctrl.GetValue()
            }\""""
        with open(self.pyttcl.ConfigFile, 'w', encoding='UTF-8') as f:
            self.pyttcl.Config.write(f)
        self.update_servers_list()

    def update_server_info_panel(self, evt=None):
        """Update server information panel by selected item in servers list."""
        server_data = self.pyttcl.Config[
            self.get_servers_list()[self.servers_listbox.GetSelection()]
        ]
        self.hostname_textctrl.SetValue(server_data['host'])
        self.tcpport_textctrl.SetValue(server_data['tcpport'])
        self.udpport_textctrl.SetValue(server_data['udpport'])
        self.username_textctrl.SetValue(server_data['username'])
        self.password_textctrl.SetValue(server_data['password'])
        self.channel_textctrl.SetValue(server_data['channel'])
        self.channel_password_textctrl.SetValue(
            server_data['channel_password']
        )
        self.note_name_textctrl.SetValue(server_data.name)

    def update_servers_list(self):
        """Update servers list from config."""
        selected_item = self.servers_listbox.GetSelection()
        self.servers_listbox.Items = self.get_servers_list()
        self.servers_listbox.Select(selected_item)
        self.update_server_info_panel()
