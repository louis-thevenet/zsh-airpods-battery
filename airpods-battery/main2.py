import asyncio
from bleak import BleakScanner
from binascii import hexlify
from time import sleep

AIRPODS_MANUFACTURER = 76
AIRPODS_DATA_LENGTH = 54
UPDATE_INTERVAL = 1

# Return if left and right is flipped in the data
def is_flipped(raw):
    return (int("" + chr(raw[10]), 16) & 0x02) == 0

async def get_data():
    discovered_devices_and_advertisement_data = await BleakScanner.discover(return_adv=True)
    for key, dev_and_adv_dat in discovered_devices_and_advertisement_data.items():
        device = dev_and_adv_dat[0]
        adv_dat = dev_and_adv_dat[1]
        if AIRPODS_MANUFACTURER in adv_dat.manufacturer_data.keys():
            hexa_data = hexlify(adv_dat.manufacturer_data[AIRPODS_MANUFACTURER])
            if (len(hexa_data)==AIRPODS_DATA_LENGTH):
                return hexa_data
    return None
            
def process_hexa(data_hexa):
    flip: bool = is_flipped(data_hexa)

    # On 7th position we can get AirPods model, gen1, gen2, Pro or Max
    if chr(data_hexa[7]) == '4':
        model = "AirPodsPro2"
    elif chr(data_hexa[7]) == 'e':
        model = "AirPodsPro"
    elif chr(data_hexa[7]) == '3':
        model = "AirPods3"
    elif chr(data_hexa[7]) == 'f':
        model = "AirPods2"
    elif chr(data_hexa[7]) == '2':
        model = "AirPods1"
    elif chr(data_hexa[7]) == 'a':
        model = "AirPodsMax"
    else:
        model = "unknown"

    # Checking left AirPod for availability and storing charge in variable
    status_tmp = int("" + chr(data_hexa[12 if flip else 13]), 16)
    left_status = (100 if status_tmp == 10 else (status_tmp * 10 + 5 if status_tmp <= 10 else -1))

    # Checking right AirPod for availability and storing charge in variable
    status_tmp = int("" + chr(data_hexa[13 if flip else 12]), 16)
    right_status = (100 if status_tmp == 10 else (status_tmp * 10 + 5 if status_tmp <= 10 else -1))

    # Checking AirPods case for availability and storing charge in variable
    status_tmp = int("" + chr(data_hexa[15]), 16)
    case_status = (100 if status_tmp == 10 else (status_tmp * 10 + 5 if status_tmp <= 10 else -1))

    # On 14th position we can get charge status of AirPods
    charging_status = int("" + chr(data_hexa[14]), 16)
    charging_left:bool = (charging_status & (0b00000010 if flip else 0b00000001)) != 0
    charging_right:bool = (charging_status & (0b00000001 if flip else 0b00000010)) != 0
    charging_case:bool = (charging_status & 0b00000100) != 0

    
    return dict(
        status=1,
        charge=dict(
            left=left_status,
            right=right_status,
            case=case_status
        ),
        charging_left=charging_left,
        charging_right=charging_right,
        charging_case=charging_case,
        model=model,
        raw=data_hexa.decode("utf-8")
    )

async def main():
    with open('battery_data', 'w') as writer:
        while True:
            res=await get_data()
            writer.seek(0)
            if res is not None:
                writer.write("works")
            else:
                writer.write("works2")
            writer.truncate()
        sleep(UPDATE_INTERVAL)



asyncio.run(main())