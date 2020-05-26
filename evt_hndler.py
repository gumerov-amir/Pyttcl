from threading import Thread

from wx import CallAfter

from msg_dlg import MessageDialog

from  TeamTalk5 import Channel, User

import Tolk


class EventThread(Thread):
    def __init__(self, pyttcl):
        Thread.__init__(self    )
        self.Pyttcl = pyttcl
        self.allow_notify = True

    def run(self):
        while True:
            msg = self.Pyttcl.TeamTalk.getMessage()
            if msg.nClientEvent > 0:
                self.handleEvent(msg)

    def handleEvent(self, msg):
        if msg.nClientEvent == 10:
            self.notify(_('Connected'))
            self.Pyttcl.is_connected = True
        elif msg.nClientEvent == 20:
            self.notify(_('Not connected'))
            self.Pyttcl.is_connected = False
        elif msg.nClientEvent == 210:
            self.notify("error" +  str(msg.__dict__))
        elif msg.nClientEvent == 220:
            pass
        elif msg.nClientEvent == 230:
            self.notify(_('loggedin'))
            self.Pyttcl.is_loggedin = True
        elif msg.nClientEvent == 280:
            self.updateUser(msg.user)
        elif msg.nClientEvent == 290:
            self.joinUser(msg.user)
        elif msg.nClientEvent == 310:
            CallAfter(lambda pyttcl, arg: MessageDialog(pyttcl, arg.textmessage), self.Pyttcl, msg)
        elif msg.nClientEvent == 320:
            self.addChannelToTreeview(msg.channel)

    def notify(self, txt):
        if self.allow_notify:
            Tolk.speak(txt)

    def addChannelToTreeview(self, channel):
        if channel.nChannelID == 1:
            self.Pyttcl.MainTreeviewData[
                self.Pyttcl.GUI.Frame.Tree.AddRoot(
                    f'{self.Pyttcl.TeamTalk.getServerProperties().szServerName} ({len(self.Pyttcl.TeamTalk.getServerUsers())})'
                )
            ] = channel
            self.Pyttcl.MessageData['C'][channel.nChannelID] = {}
        elif channel.nChannelID != 1 and channel.nParentID == 1:
            self.Pyttcl.MainTreeviewData[
                self.Pyttcl.GUI.Frame.Tree.AppendItem(
                    self.Pyttcl.GUI.Frame.Tree.GetRootItem(),
                    f'{channel.szName} ({len(self.Pyttcl.TeamTalk.getChannelUsers(channel.nChannelID))})'
                )
            ] = channel
            self.Pyttcl.MessageData['C'][channel.nChannelID] = {}
        else:
            for parentChannel in list(self.Pyttcl.MainTreeviewData.keys()):
                if self.Pyttcl.MainTreeviewData[parentChannel].nChannelID == channel.nParentID:
                    self.Pyttcl.MainTreeviewData[
                        self.Pyttcl.GUI.Frame.Tree.AppendItem(
                            parentChannel,
                            f'{channel.szName} ({len(self.Pyttcl.TeamTalk.getChannelUsers(channel.nChannelID))})'
                        )
                    ] = channel
                    self.Pyttcl.MessageData['C'][channel.nChannelID] = {}

    def joinUser(self, user):
        if user.nUserID in [u.nUserID if type(u) ==User else -1 for u in self.Pyttcl.MainTreeviewData.values()]:
            self.Pyttcl.GUI.Frame.Tree.Delete(list(self.Pyttcl.MainTreeviewData.keys())[[u.nUserID if type(u) ==User else -1 for u in self.Pyttcl.MainTreeviewData.values()].index(user.nUserID)])
        for         i in list(self.Pyttcl.MainTreeviewData.keys()):
            if type(self.Pyttcl.MainTreeviewData[i]) ==Channel and user.nChannelID == self.Pyttcl.MainTreeviewData[i].nChannelID:
                self.Pyttcl.MainTreeviewData[
                    self.Pyttcl.GUI.Frame.Tree.AppendItem(
                        i,
                        user.szNickname
                    )
                ] = user
                if user.nUserID not in self.Pyttcl.MessageData['U'].keys():
                    self.Pyttcl.MessageData['U'][user.nUserID] = {}
                break

    def updateUser(self, user):
        for item in list(self.Pyttcl.MainTreeviewData.keys()):
            if type(self.Pyttcl.MainTreeviewData[item]) ==User and self.Pyttcl.MainTreeviewData[item].nUserID == user.nUserID:
                self.Pyttcl.GUI.Frame.Tree.SetItemText(item, user.szNickname)
