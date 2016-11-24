# SSH Poweroff
This utility exposes a webpage that gives the possibility to launch commands to
different devices in the network by means of the ssh protocol.

It has been created in order to launch a `poweroff` command to a list of video
projectors.

## Requirements
The project is exclusively tested on Debian 8 Jessie.

- `Python` >= `3.4`
- `systemd` >= `215`
- `Flask` >= `0.11.1`
- `gunicorn` >= `19.6.0`
- `pexpect` >= `4.2.1`
- `PyYAML` >= `3.11`

## Installation
To begin the installation, `su` into root account and install `curl`.
If you are on Debian:

```shell
apt-get install -y curl
```

Or if you are on Arch Linux

```shell
pacman -S --noconfirm curl
```

Then launch the following command:

```shell
curl -sL https://gitlab.com/datasoftsrl/ssh-poweroff/raw/master/install.py | python3 -
```

**NOTE**: do not forget to edit the configuration file (see next paragraph).

## Configuration
Configuration is to be written in the YAML format.

Config is read from a file located in the installation path (by default
`/opt/ssh-poweroff/config.yml`) and a commented example is provided.

**NOTE**: the YAML format does not accept tabs, so do not use them, use spaces
instead.

## Usage
After installation the software should be already started and activated.

### Starting/stopping SystemD service
To start the service use `systemctl start sshpoff` and to stop
`systemctl stop sshpoff`.

### When config is updated
Remember to `systemctl restart sshppoff` when `config.yml` is modified.

### Error log
To see error log use SystemD log facility, with the command:

```shell
journalctl -xeb -u sshpoff
```

**NOTE**: with this command you will display only this application log, from
last boot to now.

Or:

```shell
systemctl status sshpoff
```

## Uninstallation
To uninstall this software go to installation dir (default to
`/opt/ssh-poweroff` and launch this command:

```shell
python3 uninstall.py
```
