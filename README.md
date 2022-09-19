## C-863 Mercury Servo Controller daemon

`c863_focusd` interfaces with and wraps a Physik Instrumente C-863 Mercury Servo Controller and exposes it via Pyro.

`focus` is a commandline utility for controlling the focuser.

### Configuration

Configuration is read from json files that are installed by default to `/etc/focusd`.
A configuration file is specified when launching the server, and the `focus` frontend will search this location when launched.

The configuration options are:
```python
{
  "daemon": "onemetre_red_focuser", # Run the server as this daemon. Daemon types are registered in `rockit.common.daemons`.
  "log_name": "focusd@onemetre", # The name to use when writing messages to the observatory log.
  "control_machines": ["OneMetreTCS", "OneMetreDome"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `rockit.common.IP`.
  "serial_port": "/dev/focuser", # Serial FIFO for communicating with the focuser
  "serial_baud": 9600, # Serial baud rate (always 9600)
  "serial_timeout": 5, # Serial comms timeout
  "nominal_focus_position": 9000, # Position to move to after homing
  "max_position": 10000000, # Maximum allowable position
  "moving_loop_delay": 0.5, # Delay in seconds between focuser status polls when moving
  "move_timeout": 180, # Maximum time expected for a focus movement
}

```

## Initial Installation


The automated packaging scripts will push 4 RPM packages to the observatory package repository:

| Package                           | Description                                                                  |
|-----------------------------------|------------------------------------------------------------------------------|
| rockit-focuser-c863-server        | Contains the `c863_focusd` server and systemd service file.                  |
| rockit-focuser-c863-client        | Contains the `focus` commandline utility for controlling the focuser server. |
| python3-rockit-focuser-c863       | Contains the python module with shared code.                                 |
| rockit-focuser-c863-data-onemetre | Contains the json configuration for the W1m telescope.                       |

After installing packages, the systemd service should be enabled:

```
sudo systemctl enable --now c863_focusd@<config>
```

where `config` is the name of the json file for the appropriate telescope.

Now open a port in the firewall:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```
where `port` is the port defined in `rockit.common.daemons` for the daemon specified in the config.

### Upgrading Installation

New RPM packages are automatically created and pushed to the package repository for each push to the `master` branch.
These can be upgraded locally using the standard system update procedure:
```
sudo yum clean expire-cache
sudo yum update
```

The daemon should then be restarted to use the newly installed code:
```
sudo systemctl restart c863_focusd@<config>
```

### Testing Locally

The camera server and client can be run directly from a git clone:
```
c863_focusd test.json
FOCUSD_CONFIG_PATH=./test.json ./focus status
```
