# -*- coding: UTF-8 -*-

"""A python TeamTalk5 Client."""

import configparser
import gettext
import os
import sys


from GUI import GUI

import TeamTalk5


class pyttcl:
    """Class that defines the application."""

    def __init__(self, config_file='pyttcl.ini'):
        """Initialize App.

        if config_file selected it will be used
        """
        self.Config = configparser.ConfigParser()
        self.Config.read(config_file, encoding='UTF-8')
        self.Translation = gettext.translation(
            'pyttcl', 'locale', languages=[self.Config.get(
                'settings', 'language'
            )]
        )
        self.Translation.install()
        TeamTalk5.setLicense('BearWare.dk', '4f30b90b')
        self.TeamTalk = TeamTalk5.TeamTalk()
        self.GUI = GUI(self)
        self.MainTreeviewData = {}
        self.MessageData = {'C': {}, 'U': {}, 'W': {'C': {}, 'U': {}}}
        self.is_connected = None
        self.is_loggedin = None
        self.GUI.MainLoop()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        pyttcl()
    elif len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            pyttcl(sys.argv[1])
        elif sys.argv[1] == '--help':
            print(
                'pyttcl- a client for TeamTalk\n\
for running pyttcl with your config file use:\n\
pyttcl.py path\\your_file.ini'
            )
    else:
        print('use --help for get help')
