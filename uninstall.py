#!/usr/bin/env python3

import sys, os
import shutil as sh, subprocess as sp
from os import path

PATH = '/opt/ssh-poweroff'
WD = '/tmp/ssh-poweroff'

def msg(message, dots=True):
  _dots = "."
  if dots:
    _dots = '...'
  print('[*] {}{}'.format(message, _dots))

def ok():
  msg('done', dots=True)

def errror(message):
  print('[!] error: {}.'.format(message))

def cmd(command):
  sp.check_call(command, stdin=sp.DEVNULL, stdout=sp.DEVNULL,
    stderr=sp.DEVNULL)

if __name__ == '__main__':
  if os.geteuid() == 0:
    try:
      # remove temporary and permanent repos
      msg('removing {}'.format(WD))
      sh.rmtree(WD, ignore_errors=True)
      ok()

      msg('removing {}'.format(PATH))
      sh.rmtree(PATH, ignore_errors=True)
      ok()

      # disactivate systemd service
      msg('stopping and disabling service')
      cmd(['systemctl', 'stop', 'sshpoff'])
      cmd(['systemctl', 'disable', 'sshpoff'])
      ok()

      msg('messing with systemd')
      # remove unit file (and ignore errors)
      try:
        os.remove('/etc/systemd/system/sshpoff.service')
      except:
        pass
      # reload systemd units
      cmd(['systemctl', 'daemon-reload'])
      ok()
    except Exception as e:
      print(e)
      sys.exit(255)
  else:
    error('This script must be run as root.')
