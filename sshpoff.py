#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys, random
from os import path

import yaml
from flask import (
  Flask,
  request,
  render_template
)
from pexpect.pxssh import (
  pxssh,
  ExceptionPxssh
)

VERSION = '1.1.0'

CONF_PATH = path.join(
  path.dirname(__file__),
  'config.yml'
)

app = Flask(__name__)

"""
Load config and throw an error if config is not good.
"""
try:
  config = yaml.safe_load(open(CONF_PATH))
except:
  print(
    'Ops, I found an error reading {}, using default.'.format('config.yml'),
    file=sys.stderr
  )
  config = {}

"""
Check if config key is present, otherwise use default.
"""
default = {
  'title': 'Poweroff',
  'devices': [],
  'command': {
    'shutdown': 'halt'
  }
}
default.update(config)
config = default
del default

"""
Cache a 'devices' dict for ease of use.
"""
if len(config['devices']) > 0:
  devices = {x['name']: x for x in config['devices']}
else:
  devices = {}

def _random_colors():
  """
  Returns a generators with names of random colors.
  """
  colors = [
    'red',
    'pink',
    'deep-purple',
    'indigo',
    'blue',
    'light-blue',
    'cyan',
    'teal',
    'green',
    'light-green',
    'orange',
    'deep-orange',
    'brown',
    'blue-grey'
  ]

  random.shuffle(colors)
  
  count = 0
  length = len(colors)
  while True:
    if count == length:
      count = 0
    yield colors[count]
    count += 1

@app.route('/')
def home():
  """
  If called with GET method, it show buttons.
  If called with POST method, it processes the action given by the button
  pressed.
  """
  global config

  return render_template('index.html',
    title = config['title'],
    version = VERSION,
    devices = zip(_random_colors(), config['devices']),
    command = 'shutdown'
  )

@app.route('/command', methods=['POST'])
def command():
  """
  Executes a command to a given device (form field 'id') when triggered.
  """
  global config, devices

  if request.method == 'POST':
    name = request.form['id']
    try:
      properties = devices[name]
      ssh = pxssh()
      ssh.force_password = True
      ssh.options['StrictHostKeyChecking'] = 'no'
      ssh.login(
        server = properties['host'],
        username = properties['user'],
        password = properties['password'],
        port = properties['port']
      )
      ssh.sendline(properties['command'])
      ssh.logout()
      return '{} successfully turned off.'.format(name)
    except (KeyError, ExceptionPxssh) as e:
      if isinstance(e, KeyError):
        return '{} does not exist!'.format(name)
      elif isinstance(e, ExceptionPxssh):  
        return 'Could not communicate with {}!'.format(name)
