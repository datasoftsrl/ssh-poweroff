# SSH Poweroff
This utility exposes a webpage that gives the possibility to launch commands to
different devices in the network by means of the ssh protocol.

It has been created in order to launch a `poweroff` command to a list of video
projectors.

## Requirements
The project is exclusively tested on Debian 8 Jessie.

- `Python` >= `3.5`
- `systemd` >= `215`
- `Flask` >= `0.11.1`
- `gunicorn` >= `19.6.0`
- `pexpect` >= `4.2.1`
- `PyYAML` >= `3.11`

## Installation
To begin the installation, `su` into root account, `cd` to a writable folder
(`/tmp` should be perfect) and launch the following command:

`curl -sL https://gitlab.com/datasoftsrl/projector-poweroff/raw/master/install.py | python -`

Do not forget to edit the configuration file.

## Configuration
Configuration is to be written in the YAML format.

Config is read from a file located in the installation path (by default
`/opt/projector-poweroff/config.yml`) and a commented example is provided.

**NOTE**: the YAML format does not accept tabs, so do not use them, use spaces
instead.

## Usage
After installation the software should be already started and activated.

To start the service use `systemctl start ppoff` and to stop
`systemctl stop ppoff`.

Remember to `systemctl restart ppoff` when `config.yml` is modified.

To see error log use SystemD log facility, with the command:

`journalctl -xeb -u ppoff`

**NOTE**: with this command you will display only this application log, from
last boot to now.
