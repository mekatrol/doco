
```bash
sudo nano /etc/systemd/timesyncd.conf
```

> Root distance needs to be high for local stratum 1 from raspberry PI client (sounds stupid)

```ini
[Time]  
NTP=ntp.home.wojcik.com.au  
RootDistanceMaxSec=60  
```
