#!/usr/bin/env python3

import sys, os, platform
import shutil as sh, subprocess as sp
from os import path

import yaml

PREFIX = path.dirname(path.realpath(__file__))

PATH = '/opt/ssh-poweroff'
REPO = 'https://gitlab.com/datasoftsrl/ssh-poweroff.git'
WD = '/tmp/ssh-poweroff'

def cmd(command):
  sp.run(command, stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)

if __name__ == '__main__':
  if os.geteuid() == 0:
    try:
      conf_path = path.join(
        WD,
        'config.yml'
      )
      config = yaml.safe_load(open(conf_path))
      config['port']
    except:
      config = {
        'port': 8081
      }

    try:
      # only arch linux and debian/ubuntu supported in installer
      distro = platform.linux_distribution()[0].lower()
      if distro == 'arch':
        cmd(['pacman', '-S', '--noconfirm', 'python-pip git'])
      elif distro == 'ubunutu' or distro == 'debian':
        cmd(['apt-get', 'install', '-y', 'python3-pip git'])
      else:
        print('Sorry, your distro is currently not supported with this installer.')

      # installation commands (it will remove everything in 
      cmd(['pip3', 'install', 'flask pyyaml gunicorn pexpect'])
      cmd(['git', 'clone', REPO, WD])
      cmd(['rm', '-rf', PATH])
      sh.copytree(WD, PATH)

      # write a systemd unit file
      with open(path.join(PATH, 'sshpoff.service.stub'), 'r') as r_serv:
        with open('/etc/systemd/system/sshpoff.service', 'w') as w_serv:
          lines = r_serv.read()
          w_serv.write(lines.replace('<port>', str(config['port']), 1))

      # activate systemd service
      cmd(['systemctl', 'daemon-reload'])
      cmd(['systemctl', 'enable', 'sshpoff'])
      cmd(['systemctl', 'start', 'sshpoff'])
    except Exception as e:
      print(e)
      sys.exit(255)
  else:
    print('This script must be run as root.')
