# NTP

```bash
sudo nano /etc/systemd/timesyncd.conf
```

```ini
[Time]  
NTP=ntp.lan  
```

> Get time sync status

```bash
timedatectl status

timedatectl show-timesync

sudo timedatectl set-ntp true
```

> Restart time sync service  

```bash
sudo systemctl restart systemd-timesyncd
```

> Force time update

```bash
sudo date -s '2024-12-20 10:00:00'

# OR

sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"
```
