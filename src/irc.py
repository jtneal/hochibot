#!/usr/bin/env python

import os
import re
import socket
import sys

class IRC:

  HOST = 'irc.chat.twitch.tv'
  PORT = 6667
  AUTH = os.environ['TWITCH_OAUTH_TOKEN']
  NICK = 'hochibot'

  def validate_login(self, data):
    if re.match(r'^:(tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$', data):
      return False
    else:
      return True

  def make_command(self, command):
    return bytes(command + '\r\n', 'UTF-8')

  def getConnection(self):
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
      irc.connect((self.HOST, self.PORT))
    except:
      print('Cannot connect to server (%s:%s).' % (self.HOST, self.PORT), 'error')
      sys.exit()

    irc.send(self.make_command('USER %s' % self.NICK))
    irc.send(self.make_command('PASS oauth:%s' % self.AUTH))
    irc.send(self.make_command('NICK %s' % self.NICK))

    if self.validate_login(irc.recv(1024).decode('UTF-8')):
      print('Login successful.')
    else:
      print('Login unsuccessful.')
      sys.exit()

    return irc
