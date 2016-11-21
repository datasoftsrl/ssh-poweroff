#!/usr/bin/env python3

import sys, os, platform
import shutil as sh, subprocess as sp
from os import path

PREFIX = path.dirname(path.realpath(__file__))

PATH = '/opt/projector-poweroff'
REPO = 'https://gitlab.com/datasoftsrl/projector-poweroff.git'
WD = path.join(PREFIX, 'projector-poweroff')

if __name__ == '__main__':

  if os.geteuid() == 0:
    try:
      # only arch linux and debian/ubuntu supported in installer
      distro = platform.linux_distribution()[0].lower()
      if distro == 'arch':
        sp.run(['pacman', '-S', '--noconfirm', 'python-pip git'],
          stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
      elif distro == 'ubunutu' or distro == 'debian':
        sp.run(['apt-get', 'install', '-y', 'python3-pip git'],
          stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
      else:
        print('Sorry, your distro is currently not supported with this installer.')

      # installation commands (it will remove everything in 
      sp.run(['pip3', 'install', 'flask pyyaml gunicorn pexpect'],
        stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
      sp.run(['git', 'clone', REPO, WD],
        stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
      sp.run(['rm', '-rf', PATH],
        stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
      sh.copytree(WD, PATH)
      sh.copy(path.join(PATH, 'ppoff.service'), '/etc/systemd/system')
      sp.run(['systemctl', 'daemon-reload'],
        stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
      sp.run(['systemctl', 'enable', 'ppoff'],
        stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
      sp.run(['systemctl', 'start', 'ppoff'],
        stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    except Error as e:
      print(e)
      sys.exit(255)
  else:
    print('This script must be run as root.')
