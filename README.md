# zsh-airpods-battery
Zsh plugin that looks for Airpods via bluetooth and displays their battery in RPROMPT. The plugin is mainly for personnal use although I provided some installation information. \
It is probably not compatible with powerlevel9k or anything that uses the RPROMPT variable.

Because of Apple's decisions toward non Apple devices interacting with airpods, fetched values go from 0 to 10 resulting in a &pm;5% precision. 

![image](https://github.com/A-delta/zsh-airpods-battery/assets/55986107/30f964b5-6085-4760-9a74-14148942cd49)

## Installation
### Zsh plugin
###  Python script

You can run simply the script `python3 fetch_airpods_battery.py` or you can make it more permanent by installing it as a service.

Edit the `airpods-battery-fetcher.service` service file template:
```
[Unit]
Description=AirPods Battery Fetcher for zsh plugin zsh-airpods-battery

[Service]
ExecStart=/usr/bin/python3 /PATH/TO/fetch_airpods_battery.py /tmp/airpods_battery.out # EDIT SCRIPT PATH HERE
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```

Create `/etc/systemd/system/airpods-battery-fetcher.service` file:
`sudo mv airpods-battery-fetcher.service /etc/systemd/system/airpods-battery-fetcher.service`

Enable service on boot:
`sudo systemctl start airpods-battery-fetcher.service`

Start service:
`sudo systemctl start airpods-battery-fetcher`

