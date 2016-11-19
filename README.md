# Project Poweroff
This utility exposes a webpage that gives the possibility to launch commands to
different devices in the network by means of the ssh protocol.

It has been created in order to launch a `poweroff` command to a list of video
projectors.

## Requirements
The project is exclusively tested on Debian 8 Jessie.

- `Python` >= `2.5`
- `systemd` >= `215`
- `Flask` >= `0.11.1`
- `gunicorn` >= `19.6.0`
- `pexpect` >= `4.2.1`
- `PyYAML` >= `3.11`
