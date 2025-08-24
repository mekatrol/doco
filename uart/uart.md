# Configure UART on RPI Zero

## Connections (TTL side)

> Pi Zero GPIO14 (TXD0, pin 8) → Target RX  
> Pi Zero GPIO15 (RXD0, pin 10) ← Target TX  
> Ground → Ground  

⚠️ Logic is 3.3 V. If your target device is 5 V TTL, use a level shifter.

```bash
 sudo nano  /boot/firmware/config.txt
```

```bash
enable_uart=1
```

```bash
sudo nano /boot/firmware/cmdline.txt
```

Make sure there is no `console=serial0,115200` in the line.
It must remain a single line, so just remove that part — don’t add line breaks.

```bash
sudo systemctl stop serial-getty@serial0.service
sudo systemctl disable serial-getty@serial0.service
```

After reboot, you should have `/dev/serial0`.

## Run pass through between uarts

```bash
sudo apt install python3-serial -y
```

```bash
python ./uart_passthrough.py
```
