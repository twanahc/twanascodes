# -*- coding: utf-8 -*-

import logging
import asyncio
import platform
import ast

from bleak import BleakClient
from bleak import BleakScanner
from bleak import discover

# These values have been randomly generated - they must match between the Central and Peripheral devices
# Any changes you make here must be suitably made in the Arduino program as well
Data_UUID = 'de198f3d-69ff-497c-9c2e-3fcf79013af9'

vc2,vc3 = 13.28,13.28 ## volumes of channels mm2

def getValue(on):
    if on:
        return on_value
    else:
        return off_value


async def run():
    k = 0
    sumt = 0
    timelist =[]
    print('Looking for the Arduino Nano...')

    found = False
    devices = await discover()
    for d in devices:
        if 'Arduino'in d.name:
            print('Found it!')
            found = True
            async with BleakClient(d.address) as client:

                print(f'Connected to {d.address}')
                while True:
                    val = await client.read_gatt_char(Data_UUID) #get data
                    #print(val)
                    val= int.from_bytes(val, byteorder = "little") #convert to integer from bytes
                    val = val/100000; #The dividing value is dependent on how much we scale the value with in the arduino,
                    # If you change the scaling value here or in the arduino, make sure that you change it on both places!
                    print("Flowrate: " + str(val) + " mm3/uL per second6 ")


    if not found:
        print('Could not find the Arduino Nano')


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run())
except KeyboardInterrupt:
    print('\nReceived Keyboard Interrupt')
finally:
    print('Program finished')
