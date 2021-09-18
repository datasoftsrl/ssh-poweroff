#!/usr/bin/env python3

import sys, os, platform
import shutil as sh, subprocess as sp
from os import path

REPO = 'https://gitlab.com/datasoftsrl/ssh-poweroff.git'
PATH = '/opt/ssh-poweroff'
WD = '/tmp/ssh-poweroff'

def msg(message, dots=True):
  _dots = "."
  if dots:
    _dots = '...'
  print('[*] {}{}'.format(message, _dots))

def ok():
  msg('done', dots=False)

def errror(message):
  print('[!] error: {}.'.format(message))

def cmd(command):
  return sp.check_call(command, stdin=sp.DEVNULL, stdout=sp.DEVNULL,
    stderr=sp.DEVNULL)

if __name__ == '__main__':
  if os.geteuid() == 0:
    try:
      # prefix at which python executables are saved
      prefix = '/usr/local'
      # only arch linux and debian/ubuntu supported in installer
      distro = platform.linux_distribution()[0].lower()
      if distro == 'arch':
        msg('installing git and pip with pacman')
        cmd(['pacman', '-S', '--noconfirm', 'python-pip', 'git'])
        prefix = '/usr'
        ok()
      elif distro == 'ubuntu' or distro == 'debian':
        msg('installing git and pip3 with apt')
        cmd(['apt-get', 'install', '-y', 'python3-pip', 'git'])
        ok()
      else:
        error('sorry, your distro is currently not supported with this installer')

      # installation commands (it will remove everything in PATH)
      msg('installing flask, pyyaml, gunicorn and pexpect with pip3')
      cmd(['pip3', 'install', 'flask', 'pyyaml', 'gunicorn', 'pexpect'])
      ok()
      
      msg('cloning git repository into {}'.format(WD))      
      cmd(['git', 'clone', REPO, WD])
      ok()
      
      # read config
      import yaml
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

      msg('copying repository into {}'.format(PATH))
      sh.rmtree(PATH, ignore_errors=True)
      sh.copytree(WD, PATH)
      ok()

      # write a systemd unit file
      msg('messing with systemd')
      with open(path.join(PATH, 'sshpoff.service.stub'), 'r') as r_unit:
        with open('/etc/systemd/system/sshpoff.service', 'w') as w_unit:
          lines = r_unit.read()
          lines = (
            lines.replace('<prefix>', prefix, 1)
                 .replace('<port>', str(config['port']), 1)
          )
          w_unit.write(lines)
      ok()

      # activate systemd service
      msg('enabling and starting service')
      cmd(['systemctl', 'daemon-reload'])
      cmd(['systemctl', 'enable', 'sshpoff'])
      cmd(['systemctl', 'start', 'sshpoff'])
      ok()
    except Exception as e:
      print(e)
      sys.exit(255)
  else:
    error('this script must be run as root')
