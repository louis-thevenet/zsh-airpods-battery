# zsh-airpods-battery

## Python script

The Python script can be used to retrieve your Airpods' battery level. I personally don't use the Zsh plugin part anymore.

Get current battery level: `python3 ./fetch_airpods_battery.py`

Have the script contiuously write it to a file: `python3 ./fetch_airpods_battery.py > ./out`

The latter one can be useful in a Waybar config for example.

## Zsh plugin

`./airpods-battery.plugin.zsh` is zsh plugin that looks for Airpods via bluetooth and displays their battery in RPROMPT.

It is probably not compatible with powerlevel9k or anything that uses the RPROMPT variable.

Because of Apple's decisions toward non Apple devices interacting with airpods, fetched values only go from 0 to 10 resulting in a &pm;5% precision.

![image](https://github.com/A-delta/zsh-airpods-battery/assets/55986107/d378fe21-a24a-4725-b971-098d2bfc925a)
![image](https://github.com/A-delta/zsh-airpods-battery/assets/55986107/0d665959-9018-4782-85d2-73abd167c081)

## Installation for Zsh

### With oh-my-zsh

```
git clone https://github.com/A-delta/zsh-airpods-battery.git ~/.oh-my-zsh/custom/plugins/airpods-battery
```

And add `airpods-battery` to `plugins` in `.zshrc`.

### Python script installation

You can simply run the script via `python3 fetch_airpods_battery.py --format zsh > /tmp/airpods_battery.out` or you can install it as a service:

Edit the following `airpods-battery-fetcher.service` service file template:

```
[Unit]
Description=AirPods Battery Fetcher for zsh plugin zsh-airpods-battery

[Service]
ExecStart=/usr/bin/python3 /PATH/TO/fetch_airpods_battery.py --format zsh > /tmp/airpods_battery.out
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```

Move the service file to correct location:

```
mv airpods-battery-fetcher.service /etc/systemd/user/airpods-battery-fetcher.service
```

Start service:

```
systemctl --user start airpods-battery-fetcher.service
```

Enable service on boot:

```
systemctl --user enable airpods-battery-fetcher.service
```

## Python Script Installation for Standalone use

Install the service the same way as before except for the `ExecStart` part. Replace it with `ExecStart=/usr/bin/python3 /PATH/TO/fetch_airpods_battery.py  > /tmp/airpods_battery.out` to use ANSI colors.
