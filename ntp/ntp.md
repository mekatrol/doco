
```bash
nano /etc/systemd/timesyncd.conf:
```

> Root distance needs to be high for local stratum 1 from raspberry PI client (sounds stupid)

```ini
[Time]  
NTP=10.2.2.200  
# FallbackNTP=  
RootDistanceMaxSec=60  
```
