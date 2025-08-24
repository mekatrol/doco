# Configuring XBOX One bluetooth controller

## Update and install needed packages
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install bluetooth bluez bluez-tools python3-dbus -y
```

## Put Xbox controller into pairing mode

Hold the Xbox button until it turns on.

Hold the pair button (small button on top near LB/RB) until the Xbox button flashes quickly.

## Scan for controller

Enter the Bluetooth control shell:

```bash
bluetoothctl
```


Inside, type:

```bash
power on
agent on
default-agent
scan on
```

You’ll see lines like:

```bash
[NEW] Device XX:XX:XX:XX:XX:XX Xbox Wireless Controller
```

## Pair and trust controller

Still inside bluetoothctl:

```bash
pair XX:XX:XX:XX:XX:XX
trust XX:XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX:XX
```

Replace XX:XX... with your controller’s MAC.
If it works, the Xbox light should stop flashing and stay solid.

## Test input

Install evtest or jstest:

```bash
sudo apt install joystick -y
jstest /dev/input/js0
```

You’ll see button presses and axis movements when you use the controller.

## Auto-reconnect on boot

Once trusted, the controller should auto-reconnect.
If it doesn’t, you can add this to /etc/rc.local before exit 0:

```bash
bluetoothctl connect XX:XX:XX:XX:XX:XX
```
