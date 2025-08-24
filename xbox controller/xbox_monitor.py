#!/usr/bin/env python3
import sys
import time
import asyncio
from evdev import InputDevice, categorize, ecodes, list_devices
from evdev.events import KeyEvent, AbsEvent

# --------- Human-readable names for common Xbox controls ----------
BUTTON_NAMES = {
    ecodes.BTN_SOUTH: "A",
    ecodes.BTN_EAST: "B",
    ecodes.BTN_NORTH: "Y",
    ecodes.BTN_WEST: "X",
    ecodes.BTN_TL: "LB",
    ecodes.BTN_TR: "RB",
    ecodes.BTN_TL2: "LT (click)",
    ecodes.BTN_TR2: "RT (click)",
    ecodes.BTN_SELECT: "View/Back",
    ecodes.BTN_START: "Menu/Start",
    ecodes.BTN_MODE: "Xbox",
    ecodes.BTN_THUMBL: "LS (press)",
    ecodes.BTN_THUMBR: "RS (press)",
}

AXIS_NAMES = {
    ecodes.ABS_X: "LX",
    ecodes.ABS_Y: "LY",
    ecodes.ABS_RX: "RX",
    ecodes.ABS_RY: "RY",
    ecodes.ABS_Z: "LT",
    ecodes.ABS_RZ: "RT",
    ecodes.ABS_HAT0X: "DPad X",
    ecodes.ABS_HAT0Y: "DPad Y",
}

# Deadzone for sticks to reduce noise
STICK_DEADZONE = 2000   # out of 0..65535 if normalized later; raw varies by driver
TRIGGER_DEADZONE = 2    # out of 0..255 typical


def now():
    return time.strftime("%H:%M:%S")


def pick_device(preferred_path=None):
    """
    Try to pick an Xbox controller from /dev/input/event*.
    Priority:
      1) user-supplied path
      2) name contains 'Xbox' or 'Controller' or 'Gamepad'
    """
    if preferred_path:
        try:
            dev = InputDevice(preferred_path)
            return dev
        except Exception as e:
            print(f"[{now()}] Failed to open {preferred_path}: {e}")

    devices = [InputDevice(p) for p in list_devices()]
    if not devices:
        return None

    # sort for stable order
    devices.sort(key=lambda d: d.path)

    # Try name match
    for d in devices:
        n = (d.name or "").lower()
        if "xbox" in n or "controller" in n or "gamepad" in n:
            return d

    # Fall back: any device that has both keys and abs axes (likely a gamepad)
    for d in devices:
        caps = d.capabilities(verbose=False)
        if ecodes.EV_KEY in caps and ecodes.EV_ABS in caps:
            return d

    return None


def describe_abs(event: AbsEvent):
    name = AXIS_NAMES.get(event.event.code, f"ABS_{event.event.code}")
    val = event.event.value
    # Heuristic deadzones
    if event.event.code in (ecodes.ABS_X, ecodes.ABS_Y, ecodes.ABS_RX, ecodes.ABS_RY):
        # Many drivers use signed 16-bit for sticks: -32768..32767
        # Print raw; user can map later if needed
        return f"{name} -> {val:+d}"
    elif event.event.code in (ecodes.ABS_Z, ecodes.ABS_RZ):
        # Triggers typically 0..255
        if abs(val) < TRIGGER_DEADZONE:
            return None
        return f"{name} -> {val}"
    elif event.event.code in (ecodes.ABS_HAT0X, ecodes.ABS_HAT0Y):
        # D-Pad as hat: -1,0,1 (often -1/0/1 or -32768/0/32767 depending on driver)
        # Normalize to -1/0/1 for readability if possible
        nval = val
        if val in (-32768, 0, 32767):
            nval = -1 if val < 0 else (1 if val > 0 else 0)
        # Map to names
        if event.event.code == ecodes.ABS_HAT0X:
            direction = {-1: "Left", 0: "Center", 1: "Right"}[nval]
        else:
            direction = {-1: "Up", 0: "Center", 1: "Down"}[nval]
        return f"{name} -> {direction} ({nval})"
    else:
        return f"{name} -> {val}"


def describe_key(event: KeyEvent):
    name = BUTTON_NAMES.get(event.scancode, f"KEY_{event.scancode}")
    state = "DOWN" if event.keystate == KeyEvent.key_down else (
        "UP" if event.keystate == KeyEvent.key_up else "HOLD")
    return f"{name} {state}"


async def monitor(dev: InputDevice):
    print(f"[{now()}] Using device: {dev.path} — {dev.name}")
    print(f"[{now()}] Vendor:Product = {dev.info.vendor:04x}:{dev.info.product:04x}, version {dev.info.version}")
    print(f"[{now()}] Press Ctrl+C to quit.\n")

    async for event in dev.async_read_loop():
        if event.type == ecodes.EV_KEY:
            ev = categorize(event)
            msg = describe_key(ev)
            if msg:
                print(f"[{now()}] {msg}")
        elif event.type == ecodes.EV_ABS:
            ev = categorize(event)
            msg = describe_abs(ev)
            if msg:
                print(f"[{now()}] {msg}")
        elif event.type == ecodes.EV_SYN:
            # Frame boundary; ignore
            pass
        else:
            # Other events (e.g., MSC_SCAN), print raw for completeness
            print(
                f"[{now()}] type={event.type} code={event.code} value={event.value}")


def main():
    preferred = sys.argv[1] if len(sys.argv) > 1 else None
    dev = pick_device(preferred)
    if not dev:
        print(
            f"[{now()}] No suitable input device found. Is the controller connected and trusted?")
        print(f"Tips:")
        print(f"  1) bluetoothctl -> 'devices' should show 'Xbox Wireless Controller'")
        print(f"  2) Try: sudo evtest to see which /dev/input/event* is your controller")
        print(f"  3) Then run: {sys.argv[0]} /dev/input/eventX")
        sys.exit(1)

    try:
        asyncio.run(monitor(dev))
    except KeyboardInterrupt:
        print(f"\n[{now()}] Exiting.")
    finally:
        try:
            dev.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
