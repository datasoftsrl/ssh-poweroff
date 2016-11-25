#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys, os
import logging as lg
from os import path as ospath

class Log:

  logger = None
  handler = None
  formatter = None

  def __init__(self, name, path):
    """
    Creates a logger for name, that writes logs into path.

    < name: name of application
    < path: file where to write log
    """
    # create logger which logs all
    self.logger = lg.getLogger(name)
    self.logger.setLevel(lg.INFO)

    # create a log into path as file handler (if not possible throw exception)
    try:
      self.handler = lg.FileHandler(path)
    except:
      print('[!] error opening log file at {}.'.format(path), file=sys.stderr)
      print(
        '[!] does {} exist or have correct permissions?' \
          .format(ospath.dirname(path)),
        file=sys.stderr
      )
      sys.exit(255)

    self.handler.setLevel(lg.INFO)

    # decide log format
    self.formatter = lg.Formatter(
      fmt = \
        '%(asctime)s %(host)s %(name)s[%(pid)s]: %(levelname)s: %(message)s',
      datefmt = '%b %e %H:%M:%S'
    )
    self.handler.setFormatter(self.formatter)

    self.logger.addHandler(self.handler)

  def _write(self, func, fmt, *args):
    """
    Write a line into log of tipe INFO.

    < func: method of logger to call (info, error, etc)
    < fmt: python format string
    < *args: string to replace into fmr
    """
    
    host = os.uname()[1]
    pid = os.getpid()

    extra = {
      'host': host,
      'pid': pid
    }
    func(fmt, *args, extra=extra)

  def info(self, fmt, *args):
    self._write(self.logger.info, fmt, *args)

  def error(self, fmt, *args):
    self._write(self.logger.error, fmt, *args)
