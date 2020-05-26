import time

import wx

from TeamTalk5 import Channel, TextMessage, User


class MessageDialog(wx.Frame):
    def __init__(self, pyttcl, arg):
        if type(arg) == TextMessage:
            if arg.nMsgType == 1:
                if arg.nFromUserID not in pyttcl.MessageData['W']['U']:
                    wx.Frame.__init__(self, None, -1, _('Message from {user}'.format(user=pyttcl.TeamTalk.getUser(arg.nFromUserID).szNickname)))
                    self.Pyttcl = pyttcl
                    self.arg = arg
                    self.type = 'U'
                    self.Pyttcl.MessageData['W']['U'][arg.nFromUserID] = self
                    self.Pyttcl.MessageData['U'][self.arg.nFromUserID][time.localtime()] = self.arg
                    self.MessageHistoryCtrl = wx.TextCtrl(
                        self, -1,
                        '\n'.join(
                            f'({t.tm_hour} {t.tm_min}) {self.Pyttcl.TeamTalk.getUser(m.nFromUserID).szNickname}:\n{m.szMessage}'
                            for t,m in zip(
                                self.Pyttcl.MessageData['U'][self.arg.nFromUserID].keys(), self.Pyttcl.MessageData['U'][self.arg.nFromUserID].values()
                            )
                        ), size=(1000, 500),
                        style=wx.TE_MULTILINE | wx.TE_READONLY
                    )
                    self.NewMessageCtrl = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE)
                    sendButton = wx.Button(self, -1, _('wx.Button')) 
                    sendButton.Bind(wx.EVT_BUTTON, lambda evt: self.SendMessage())
                    closeButton = wx.Button(self, -1, _('Close'))
                    closeButton.Bind(wx.EVT_BUTTON, self.Destroy)
                    self.Show()
                else:
                    self = pyttcl.MessageData['W']['U'][arg.nFromUserID]
                    self.Pyttcl = pyttcl
                    self.arg = arg
                    self.Pyttcl.MessageData['U'][self.arg.nFromUserID][time.localtime()] = self.arg
                    self.MessageHistoryCtrl.SetValue(
                        '\n'.join(
                            f'({t.tm_hour} {t.tm_min}) {self.Pyttcl.TeamTalk.getUser(m.nFromUserID).szNickname}:\n{m.szMessage}'
                            for t,m in zip(
                                self.Pyttcl.MessageData['U'][self.arg.nFromUserID].keys(), self.Pyttcl.MessageData['U'][self.arg.nFromUserID].values()
                            )
                        )
                    )
            if arg.nMsgType == 2:
                if arg.nChannelID not in pyttcl.MessageData['W']['C']:
                    wx.Frame.__init__(self, None, -1, _('Message from {channel}'.format(channel=pyttcl.TeamTalk.getChannel(arg.nChannelID).szName)))
                    self.Pyttcl = pyttcl
                    self.arg = arg
                    self.type = 'C'
                    self.Pyttcl.MessageData['W']['C'][arg.nChannelID] = self
                    self.Pyttcl.MessageData['C'][self.arg.nChannelID][time.localtime()] = self.arg
                    self.MessageHistoryCtrl = wx.TextCtrl(
                        self, -1,
                        '\n'.join(
                            f'({t.tm_hour} {t.tm_min}) {self.Pyttcl.TeamTalk.getUser(m.nFromUserID).szNickname}:\n{m.szMessage}'
                            for t,m in zip(
                                self.Pyttcl.MessageData['C'][self.arg.nChannelID].keys(), self.Pyttcl.MessageData['C'][self.arg.nChannelID].values()
                            )
                        ), size=(1000, 500),
                        style=wx.TE_MULTILINE | wx.TE_READONLY
                    )
                    self.NewMessageCtrl = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE)
                    sendButton = wx.Button(self, -1, _('wx.Button')) 
                    sendButton.Bind(wx.EVT_BUTTON, lambda evt: self.SendMessage())
                    closeButton = wx.Button(self, -1, _('Close'))
                    closeButton.Bind(wx.EVT_BUTTON, self.Destroy)
                    self.Show()
                else:
                    self = pyttcl.MessageData['W']['C'][arg.nChannelID]
                    self.Pyttcl = pyttcl
                    self.arg = arg
                    self.Pyttcl.MessageData['C'][self.arg.nChannelID][time.localtime()] = self.arg
                    self.MessageHistoryCtrl.SetValue(
                        '\n'.join(
                            f'({t.tm_hour} {t.tm_min}) {self.Pyttcl.TeamTalk.getUser(m.nFromUserID).szNickname}:\n{m.szMessage}'
                            for t,m in zip(
                                self.Pyttcl.MessageData['C'][self.arg.nChannelID].keys(), self.Pyttcl.MessageData['C'][self.arg.nChannelID].values()
                            )
                        )
                    )
        else:
            if type(arg) == User:
                if arg.nUserID not in pyttcl.MessageData['W']['U']:
                    wx.Frame.__init__(self, None, -1, _('Message from {user}'.format(user=arg.szNickname)))
                    self.Pyttcl = pyttcl
                    self.arg = arg
                    self.type = 'U'
                    self.Pyttcl.MessageData['W']['U'][arg.nUserID] = self
                    self.MessageHistoryCtrl = wx.TextCtrl(
                        self, -1,
                        '\n'.join(
                            f'({t.tm_hour} {t.tm_min}) {self.Pyttcl.TeamTalk.getUser(m.nFromUserID).szNickname}:\n{m.szMessage}'
                            for t,m in zip(
                                self.Pyttcl.MessageData['U'][self.arg.nUserID].keys(), self.Pyttcl.MessageData['U'][self.arg.nUserID].values()
                            )
                        ), size=(1000, 500),
                        style=wx.TE_MULTILINE | wx.TE_READONLY
                    )
                    self.NewMessageCtrl = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE)
                    sendButton = wx.Button(self, -1, _('wx.Button')) 
                    sendButton.Bind(wx.EVT_BUTTON, lambda evt: self.SendMessage())
                    closeButton = wx.Button(self, -1, _('Close'))
                    closeButton.Bind(wx.EVT_BUTTON, self.Destroy)
                    self.Show()
                else:
                    self = pyttcl.MessageData['W']['U'][arg.nUserID]
                    self.Pyttcl = pyttcl
                    self.arg = arg
                    self.MessageHistoryCtrl.SetValue(
                        '\n'.join(
                            f'({t.tm_hour} {t.tm_min}) {self.Pyttcl.TeamTalk.getUser(m.nFromUserID).szNickname}:\n{m.szMessage}'
                            for t,m in zip(
                                self.Pyttcl.MessageData['U'][self.arg.nUserID].keys(), self.Pyttcl.MessageData['U'][self.arg.nUserID].values()
                            )
                        )
                    )
            if type(arg) == Channel:
                if arg.nChannelID not in pyttcl.MessageData['W']['C']:
                    wx.Frame.__init__(self, None, -1, _('Message from {channel}'.format(channel=arg.szName)))
                    self.Pyttcl = pyttcl
                    self.arg = arg
                    self.type = 'C'
                    self.Pyttcl.MessageData['W']['C'][arg.nChannelID] = self
                    self.MessageHistoryCtrl = wx.TextCtrl(
                        self, -1,
                        '\n'.join(
                            f'({t.tm_hour} {t.tm_min}) {self.Pyttcl.TeamTalk.getUser(m.nFromUserID).szNickname}:\n{m.szMessage}'
                            for t,m in zip(
                                self.Pyttcl.MessageData['C'][self.arg.nChannelID].keys(), self.Pyttcl.MessageData['C'][self.arg.nChannelID].values()
                            )
                        ), size=(1000, 500),
                        style=wx.TE_MULTILINE | wx.TE_READONLY
                    )
                    self.NewMessageCtrl = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE)
                    sendButton = wx.Button(self, -1, _('wx.Button')) 
                    sendButton.Bind(wx.EVT_BUTTON, lambda evt: self.SendMessage())
                    closeButton = wx.Button(self, -1, _('Close'))
                    closeButton.Bind(wx.EVT_BUTTON, self.Destroy)
                    self.Show()
                else:
                    self = pyttcl.MessageData['W']['C'][arg.nChannelID]
                    self.Pyttcl = pyttcl
                    self.arg = arg
                    self.MessageHistoryCtrl.SetValue(
                        '\n'.join(
                            f'({t.tm_hour} {t.tm_min}) {self.Pyttcl.TeamTalk.getUser(m.nFromUserID).szNickname}:\n{m.szMessage}'
                            for t,m in zip(
                                self.Pyttcl.MessageData['C'][self.arg.nChannelID].keys(), self.Pyttcl.MessageData['C'][self.arg.nChannelID].values()
                            )
                        )
                    )

    def Destroy(self, evt=None):
        super().Destroy()
        if self.type == 'C':
            del self.Pyttcl.MessageData['W']['C'][self.arg.nChannelID]
        elif self.type == 'U':
            del self.Pyttcl.MessageData['W']['U'][self.arg.nFromUserID]

    def SendMessage(self):
        msg = TextMessage()
        if self.type == 'C':
            msg.nMsgType = 2
            msg.nChannelID = self.arg.nChannelID
            msg.nToUserID = 0
        elif self.type == 'U':
            msg.nMsgType = 1
            msg.nChannelID = 0
            if type(self.arg) == User:
                msg.nToUserID = self.arg.nUserID
            else:
                msg.nToUserID = self.nFromUserID
        msg.nFromUserID = self.Pyttcl.TeamTalk.getMyUserID()
        msg.szFromUsername = ''
        msg.szMessage = self.NewMessageCtrl.GetValue()
        self.Pyttcl.TeamTalk.doTextMessage(msg)
        if self.type == 'C':
            self.Pyttcl.MessageData['C'][self.arg.nChannelID][time.localtime()] = msg
        else:
            if type(self.arg) == TextMessage:
                self.Pyttcl.MessageData['U'][self.arg.nFromUserID][time.localtime()] = msg
            else:
                self.Pyttcl.MessageData['U'][self.arg.nUserID][time.localtime()] = msg
        self.Update()

    def Update(self):
        if self.type == 'C':
            self.MessageHistoryCtrl.SetValue(
                '\n'.join(
                    f'({t.tm_hour} {t.tm_min}) {self.Pyttcl.TeamTalk.getUser(m.nFromUserID).szNickname}:\n{m.szMessage}'
                    for t,m in zip(
                        self.Pyttcl.MessageData['C'][self.arg.nChannelID].keys(), self.Pyttcl.MessageData['C'][self.arg.nChannelID].values()
                    )
                )
            )
        else:
            if type(self.arg) == TextMessage:
                self.MessageHistoryCtrl.SetValue(
                    '\n'.join(
                        f'({t.tm_hour} {t.tm_min}) {self.Pyttcl.TeamTalk.getUser(m.nFromUserID).szNickname}:\n{m.szMessage}'
                    for     t,m in zip(
                        self    .Pyttcl.MessageData['C'][self.arg.nChannelID].keys(), self.Pyttcl.MessageData['C'][self.arg.nChannelID].values()
                    )   
                )   
            )   
            else    :
                self    .MessageHistoryCtrl.SetValue(
                    '\n'    .join(
                        f'({    t.tm_hour} {t.tm_min}) {self.Pyttcl.TeamTalk.getUser(m.nFromUserID).szNickname}:\n{m.szMessage}'
                        for t,m     in zip(
                            self.Pyttcl.MessageData['C'][self.arg.nChannelID].keys(), self.Pyttcl.MessageData['C'][self.arg.nChannelID].values()
                    )   
                )   
            )
        self.NewMessageCtrl.Clear()
