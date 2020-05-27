# -* coding: "UTF-8" -*-

"""Module containes class that defines information dialog."""

from TeamTalk5 import Channel, User

import wx


class InfoDialog(wx.Dialog):
    """Class defines information dialog."""

    def __init__(self, pyttcl):
        """Show information about selected item in tree."""
        wx.Dialog.__init__(self, pyttcl.GUI.Frame, -1, _('Information'))
        self.Pyttcl = pyttcl
        TeamTalkItem = self.Pyttcl.MainTreeviewData[
            self.Pyttcl.GUI.Frame.Tree.GetSelection()
        ]
        if type(TeamTalkItem) == Channel:
            wx.TextCtrl(
                self, -1,
                _("""Name:
    "{name}"

Topic:
    "{topic}"

Password:
    "{password}"

Operator password:
    "{opPassword}"

Maximum users:
    "{maxUsers}"

Disk quota:
    "{diskQuota}"

Permanent channel (stored on server):
    "{v1}"

Allow only one user to transmit (no duplex):
    "{v2}"

Classroom (operator controls transmissions):
    "{v3}"

Operator receive only (only operators see and hear):
    "{v4}"

No voice activation (only Push-to-Talk allowed):
    "{v5}"

No audio recording allowed (save to disk not allowed):
    "{v6}"
""").format(
                    name=TeamTalkItem.szName,
                    topic=TeamTalkItem.szTopic,
                    password=TeamTalkItem.szPassword,
                    opPassword=TeamTalkItem.szOpPassword,
                    maxUsers=TeamTalkItem.nMaxUsers,
                    diskQuota=TeamTalkItem.nDiskQuota,
                    v1=self.getChannelTypeValue(TeamTalkItem.uChannelType, 0),
                    v2=self.getChannelTypeValue(TeamTalkItem.uChannelType, 1),
                    v3=self.getChannelTypeValue(TeamTalkItem.uChannelType, 2),
                    v4=self.getChannelTypeValue(TeamTalkItem.uChannelType, 3),
                    v5=self.getChannelTypeValue(TeamTalkItem.uChannelType, 4),
                    v6=self.getChannelTypeValue(TeamTalkItem.uChannelType, 5),
                ),
                size=(500, 500),
                style=wx.TE_MULTILINE | wx.TE_READONLY
            )
        elif type(TeamTalkItem) == User:
            wx.TextCtrl(
                self, -1,
                _("""Nickname:
    "{nickname}"

User name:
    "{userName}"

IP address:
    "{ipAddress}"

Client name:
    "{clientName}"

Type:
    "{userType}"
""").format(
                    nickname=TeamTalkItem.szNickname,
                    userName=TeamTalkItem.szUsername,
                    ipAddress=TeamTalkItem.szIPAddress,
                    clientName=TeamTalkItem.szClientName,
                    userType=[None, _('Default'), _('Admin')][
                        TeamTalkItem.uUserType
                    ]
                ),
                size=(500, 500),
                style=wx.TE_MULTILINE | wx.TE_READONLY
            )
        OkButton = wx.Button(self, -1, _('Ok'))
        OkButton.Bind(wx.EVT_BUTTON, lambda evt: self.Destroy())
        self.Bind(
            wx.EVT_CHAR_HOOK,
            lambda evt: self.Destroy() if evt.GetKeyCode() == wx.WXK_ESCAPE else evt.Skip()
        )
        self.Show()

    def getChannelTypeValue(self, nType, nPos):
        """Return Yes if the nPos with nType is True or no."""
        numbers_list = [1, 2, 4, 8, 16, 32]
        if nType in numbers_list:
            if numbers_list[nPos] == nType:
                return _('Yes')
            else:
                return _('No')
        else:
            result = []
            for number in numbers_list:
                if number + numbers_list[nPos] == nType:
                    result.append(True)
                else:
                    result.append(False)
        if any(result):
            return _('Yes')
        else:
            return _('No')
