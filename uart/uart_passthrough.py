#!/usr/bin/env python3
import serial
import select
import os

USB_DEV = "/dev/ttyACM0"     # Pi’s USB gadget endpoint
UART_DEV = "/dev/serial0"   # Pi’s GPIO UART
BAUDRATE = 115200

def main():
    usb = serial.Serial(USB_DEV, BAUDRATE, timeout=0)
    uart = serial.Serial(UART_DEV, BAUDRATE, timeout=0)

    print(f"Bridging {USB_DEV} <-> {UART_DEV} @ {BAUDRATE}bps")

    # Use select() on file descriptors for low-latency polling
    fds = [usb.fileno(), uart.fileno()]

    try:
        while True:
            rlist, _, _ = select.select(fds, [], [])
            if usb.fileno() in rlist:
                data = usb.read(usb.in_waiting or 1)
                if data:
                    uart.write(data)
            if uart.fileno() in rlist:
                data = uart.read(uart.in_waiting or 1)
                if data:
                    usb.write(data)
    except KeyboardInterrupt:
        print("\nStopping bridge...")
    finally:
        usb.close()
        uart.close()

if __name__ == "__main__":
    main()
