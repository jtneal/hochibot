#!/usr/bin/env python

from irc import IRC
import os
import re
import socket
import sys

irc = IRC()
chat = irc.getConnection()

def send(command):
  chat.send(irc.make_command(command))

def join(room):
  send('JOIN #%s' % room)
  send('PRIVMSG #%s :Kappa /' % room)

def watch():
  buffer = ''
  while True:
    buffer = buffer + chat.recv(1024).decode('UTF-8')
    temp = str.split(buffer, '\n')
    buffer = temp.pop()

    for line in temp:
      line = str.rstrip(line)
      line = str.split(line)

      if line[0] == 'PING':
        send('PONG %s' % line[1])

      if line[1] == 'PRIVMSG':

        sender = str.split(line[0], '!')
        sender = str.split(sender[0], ':')

        room = str.split(line[2], '#')

        if line[3] == ':!join' and room[1] == irc.NICK:
          join(sender[1])

        if line[3] == ':!gear':
          send('PRIVMSG %s :This is the gear.' % line[2])

        if line[3] == ':!weapon':
          send('PRIVMSG %s :This is the weapon.' % line[2])

      for index, i in enumerate(line):
        print(line[index])

join(irc.NICK)
watch()
