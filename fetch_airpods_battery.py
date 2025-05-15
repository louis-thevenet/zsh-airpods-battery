import asyncio
from bleak import BleakScanner
from binascii import hexlify
import argparse
import sys
import os
from time import sleep

AIRPODS_MANUFACTURER = 76
AIRPODS_DATA_LENGTH = 54
UPDATE_INTERVAL = 2

# ANSI color codes
RED = "\033[31m"
ORANGE = "\033[38;5;202m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
RESET = "\033[0m"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Display AirPods battery level with colored output.")
    parser.add_argument(
        "--format",
        choices=["ansi", "zsh"],
        default="ansi",
        help=
        "Output format: 'ansi' for terminal display or 'zsh' for shell prompt."
    )
    return parser.parse_args()


async def get_data_from_bluetooth():
    discovered_devices_and_advertisement_data = await BleakScanner.discover(
        return_adv=True)
    for key, dev_and_adv_dat in discovered_devices_and_advertisement_data.items(
    ):
        device = dev_and_adv_dat[0]
        adv_dat = dev_and_adv_dat[1]
        if AIRPODS_MANUFACTURER in adv_dat.manufacturer_data.keys():
            hexa_data = hexlify(
                adv_dat.manufacturer_data[AIRPODS_MANUFACTURER])
            if len(hexa_data) == AIRPODS_DATA_LENGTH and int(
                    chr(hexa_data[1]), 16) == 7:
                return hexa_data
    return None


def is_flipped(raw):
    return (int(chr(raw[10]), 16) & 0x02) == 0


def add_color_ansi(status):
    if status == '🚫':
        return status
    if status < 25:
        return f"{RED}{status}{RESET}"
    elif status < 50:
        return f"{ORANGE}{status}{RESET}"
    elif status < 75:
        return f"{YELLOW}{status}{RESET}"
    else:
        return f"{GREEN}{status}{RESET}"


def add_color_zsh(status):
    if status == '🚫':
        return status
    if status < 25:
        return f"%{{$fg[red]%}}{status}%{{$reset_color%}}"
    elif status < 50:
        return f"%{{%F{{202}}%}}{status}%{{$reset_color%}}"
    elif status < 75:
        return f"%{{$fg[yellow]%}}{status}%{{$reset_color%}}"
    else:
        return f"%{{$fg[green]%}}{status}%{{$reset_color%}}"


def get_battery_from_data(data_hexa, format_fn):
    flip: bool = is_flipped(data_hexa)

    def status_at(idx):
        value = int(chr(data_hexa[idx]), 16)
        if value == 10:
            return 100
        elif value <= 10:
            return value * 10 + 5
        else:
            return -1

    left_status = status_at(12 if flip else 13)
    right_status = status_at(13 if flip else 12)
    case_status = status_at(15)

    charging_status = int(chr(data_hexa[14]), 16)
    charging_left = (charging_status &
                     (0b00000010 if flip else 0b00000001)) != 0
    charging_right = (charging_status &
                      (0b00000001 if flip else 0b00000010)) != 0
    charging_case = (charging_status & 0b00000100) != 0

    res = ''
    if left_status != -1:
        res += f"L:{format_fn(left_status)}{'⚡' if charging_left else ''} "
    if right_status != -1:
        res += f"R:{format_fn(right_status)}{'⚡' if charging_right else ''} "
    if case_status != -1:
        res += f"C:{format_fn(case_status)}{'⚡' if charging_case else ''} "
    return res.strip()


async def main():
    args = parse_args()
    format_fn = add_color_zsh if args.format == 'zsh' else add_color_ansi
    if sys.stdout.isatty():
        res = await get_data_from_bluetooth()
        output = get_battery_from_data(
            res, format_fn) if res else "AirPods not found."
        print(output)
    else:
        while True:
            res = await get_data_from_bluetooth()
            output = get_battery_from_data(
                res, format_fn) if res else "AirPods not found."

            sys.stdout.seek(0)
            sys.stdout.write(output + '\n')
            sys.stdout.flush()
            os.ftruncate(sys.stdout.fileno(), sys.stdout.tell())

            sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting on user interrupt.")
        sys.exit(0)
