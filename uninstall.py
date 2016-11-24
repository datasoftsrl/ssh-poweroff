#!/usr/bin/env python3

import sys, os
import shutil as sh, subprocess as sp
from os import path

import yaml

PATH = '/opt/ssh-poweroff'
WD = '/tmp/ssh-poweroff'

def cmd(command):
  sp.check_call(command, stdin=sp.DEVNULL, stdout=sp.DEVNULL,
    stderr=sp.DEVNULL)

if __name__ == '__main__':
  if os.geteuid() == 0:
    try:
      # remove temporary and permanent repos
      sh.rmtree(WD, ignore_errors=True)
      sh.rmtree(PATH, ignore_errors=True)

      # disactivate systemd service
      cmd(['systemctl', 'stop', 'sshpoff'])
      cmd(['systemctl', 'disable', 'sshpoff'])
      # remove unit file (and ignore errors)
      try:
        os.remove('/etc/systemd/system/sshpoff.service')
      except:
        pass
      # reload systemd units
      cmd(['systemctl', 'daemon-reload'])
    except Exception as e:
      print(e)
      sys.exit(255)
  else:
    print('This script must be run as root.')
