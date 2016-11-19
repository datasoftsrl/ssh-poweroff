#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys
from os import path

import yaml
from flask import (
  Flask,
  render_template
)

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
  devices = {x['name']: x for x in config['devices']}
except:
  print(
    'Ops, I found an error reading {}'.format('config.yml'),
    file=sys.stderr
  )

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
    action = '/shutdown',
    devices = zip(_random_colors(), config['devices']),
    command = 'shutdown'
  )
