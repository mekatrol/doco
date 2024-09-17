# OpenWRT

1. Download Raspberry OpenWRT image and burn SD card  

> [Raspberry PI 4](https://downloads.openwrt.org/releases/23.05.4/targets/bcm27xx/bcm2711/)  

2. Configure PC to be able to talk to 192.168.1.1

> Change PC IP address to 192.168.1.10
> Connect PC to raspberry PI

3. Browse to [OpenWrt](http://192.168.1.1)

4. Log in with username: root and no password

5. Change password (you are prompted with 'Go to password configuration...')

6. Go to Network | Interfaces and edit 'lan'
   > set:
   > * IPv4 address (general settings)
   > * IPv4 gateway  (general settings)
   > * Use custom DNS servers (advanced settings)
   > save | save/apply | apply and keep settings

7. Revert PC back to original IP settings (eg DHCP) and browse to OpenWRT on the IP you set

8. Update package list and install packages

  > NOTE: using AWUS036AXML here

   click update lists  
   install packages: nano kmod-mt7921u  
   or at command line:

```bash
opkg update && opkg install usbutils nano kmod-mt7921u
```

9. Plug in dongle

10. Refresh WIFI  
```wifi```

11. Ensure WIFI devices are enabled
```nano /etc/config/wireless```

> Set: ```option disabled '0'``` on all wireless devices  

```bash
uci commit wireless
wifi
```

11. Browse to wireless settings and configure wireless:

> Connect WUS036AXML to house WIFI  
> Configure Raspberry PI WIFI as access point (make sure you set channel - auto will cause it to be disabled)  
> Make sure the Raspberry PI WIFI AP is connected to both LAN and WWAN (bridge)

12. Configure files

>*** Replace wireless passwords with real ones  

> dhcp  
> firewall  
> network  
> wireless  

13. Get copy of files

```bash
scp root@10.2.3.1:/etc/config/dhcp ./openwrt/dhcp
scp root@10.2.3.1:/etc/config/firewall ./openwrt/firewall
scp root@10.2.3.1:/etc/config/network ./openwrt/network
scp root@10.2.3.1:/etc/config/wireless ./openwrt/wireless
```
