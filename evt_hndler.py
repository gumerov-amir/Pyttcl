from threading import Thread

from wx import CallAfter

from msg_dlg import MessageDialog

from  TeamTalk5 import Channel, User

import Tolk


class EventThread(Thread):
    def __init__(self, pyttcl):
        Thread.__init__(self    )
        self.pyttcl = pyttcl
        self.allow_notify = True

    def run(self):
        while True:
            msg = self.pyttcl.TeamTalk.getMessage()
            if msg.nClientEvent > 0:
                self.handleEvent(msg)

    def handleEvent(self, msg):
        if msg.nClientEvent == 10:
            self.notify(_('Connected'))
            self.pyttcl.is_connected = True
        elif msg.nClientEvent == 20:
            self.notify(_('Not connected'))
            self.pyttcl.is_connected = False
        elif msg.nClientEvent == 210:
            self.notify("error" +  str(msg.__dict__))
        elif msg.nClientEvent == 220:
            pass
        elif msg.nClientEvent == 230:
            self.notify(_('loggedin'))
            self.pyttcl.is_loggedin = True
        elif msg.nClientEvent == 280:
            self.updateUser(msg.user)
        elif msg.nClientEvent == 290:
            self.joinUser(msg.user)
        elif msg.nClientEvent == 310:
            CallAfter(lambda pyttcl, arg: MessageDialog(pyttcl, arg.textmessage), self.pyttcl, msg)
        elif msg.nClientEvent == 320:
            self.addChannelToTreeview(msg.channel)

    def notify(self, txt):
        if self.allow_notify:
            Tolk.speak(txt)

    def addChannelToTreeview(self, channel):
        if channel.nChannelID == 1:
            self.pyttcl.MainTreeviewData[
                self.pyttcl.gui.frame.tree.AddRoot(
                    f'{self.pyttcl.TeamTalk.getServerProperties().szServerName} ({len(self.pyttcl.TeamTalk.getServerUsers())})'
                )
            ] = channel
            self.pyttcl.MessageData['C'][channel.nChannelID] = {}
        elif channel.nChannelID != 1 and channel.nParentID == 1:
            self.pyttcl.MainTreeviewData[
                self.pyttcl.gui.frame.tree.AppendItem(
                    self.pyttcl.gui.frame.tree.GetRootItem(),
                    f'{channel.szName} ({len(self.pyttcl.TeamTalk.getChannelUsers(channel.nChannelID))})'
                )
            ] = channel
            self.pyttcl.MessageData['C'][channel.nChannelID] = {}
        else:
            for parentChannel in list(self.pyttcl.MainTreeviewData.keys()):
                if self.pyttcl.MainTreeviewData[parentChannel].nChannelID == channel.nParentID:
                    self.pyttcl.MainTreeviewData[
                        self.pyttcl.gui.frame.tree.AppendItem(
                            parentChannel,
                            f'{channel.szName} ({len(self.pyttcl.TeamTalk.getChannelUsers(channel.nChannelID))})'
                        )
                    ] = channel
                    self.pyttcl.MessageData['C'][channel.nChannelID] = {}

    def joinUser(self, user):
        if user.nUserID in [u.nUserID if type(u) ==User else -1 for u in self.pyttcl.MainTreeviewData.values()]:
            self.pyttcl.gui.frame.tree.Delete(list(self.pyttcl.MainTreeviewData.keys())[[u.nUserID if type(u) ==User else -1 for u in self.pyttcl.MainTreeviewData.values()].index(user.nUserID)])
        for         i in list(self.pyttcl.MainTreeviewData.keys()):
            if type(self.pyttcl.MainTreeviewData[i]) ==Channel and user.nChannelID == self.pyttcl.MainTreeviewData[i].nChannelID:
                self.pyttcl.MainTreeviewData[
                    self.pyttcl.gui.frame.tree.AppendItem(
                        i,
                        user.szNickname
                    )
                ] = user
                if user.nUserID not in self.pyttcl.MessageData['U'].keys():
                    self.pyttcl.MessageData['U'][user.nUserID] = {}
                break

    def updateUser(self, user):
        for item in list(self.pyttcl.MainTreeviewData.keys()):
            if type(self.pyttcl.MainTreeviewData[item]) ==User and self.pyttcl.MainTreeviewData[item].nUserID == user.nUserID:
                self.pyttcl.gui.frame.tree.SetItemText(item, user.szNickname)
