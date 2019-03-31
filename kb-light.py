#!/usr/bin/env python3

import dbus
import sys


def get_kbd_backlight():
    bus = dbus.SystemBus()
    kbd_backlight_proxy = bus.get_object(
        'org.freedesktop.UPower',
        '/org/freedesktop/UPower/KbdBacklight')
    kbd_backlight = dbus.Interface(
        kbd_backlight_proxy,
        'org.freedesktop.UPower.KbdBacklight')
    return kbd_backlight


def kb_light_set(delta):
    kbd_backlight = get_kbd_backlight()

    current = kbd_backlight.GetBrightness()
    maximum = kbd_backlight.GetMaxBrightness()
    new = max(0, min(current + delta, maximum))

    if 0 <= new <= maximum:
        current = new
        kbd_backlight.SetBrightness(current)

    # Return current backlight level percentage
    return 100 * current / maximum


def kb_toggle():
    kbd_backlight = get_kbd_backlight()

    current = kbd_backlight.GetBrightness()
    maximum = kbd_backlight.GetMaxBrightness()

    new = 100 * (current / maximum) + 50
    if new > 101:
        new = 0

    current = new * maximum / 100
    kbd_backlight.SetBrightness(current)
    return 100 * current / maximum


if __name__ == '__main__':
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        if sys.argv[1] == "--up" or sys.argv[1] == "+":
            if len(sys.argv) == 3:
                print(kb_light_set(int(sys.argv[2])))
            else:
                print(kb_light_set(17))
        elif sys.argv[1] == "--down" or sys.argv[1] == "-":
            if len(sys.argv) == 3:
                print(kb_light_set(-int(sys.argv[2])))
            else:
                print(kb_light_set(-17))
        else:
            print("Unknown argument:", sys.argv[1])
    elif len(sys.argv) == 1:
        print(kb_toggle())
    else:
        print(
            "Script takes one or two argument.",
            len(sys.argv) - 1,
            "arguments provided.")
