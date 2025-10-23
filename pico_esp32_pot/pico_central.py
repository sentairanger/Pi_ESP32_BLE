import aioble
import bluetooth
import asyncio
import struct  
import json
from machine import Pin

led = Pin("LED", Pin.OUT)

connected = False

with open("uuids.json", mode="r", encoding="utf-8") as read_file:
    uuids_data = json.load(read_file) 

IAM = "Central"

MESSAGE = f"Hello from {IAM}!"

IAM_SENDING_TO = "Peripheral"

MESSAGE = f"Hello from {IAM}!"

BLE_NAME = f"{IAM}"
BLE_SVC_UUID = bluetooth.UUID(uuids_data["service"])
BLE_CHARACTERISTIC_UUID = bluetooth.UUID(uuids_data["characteristic"])
BLE_APPEARANCE = 0x0300
BLE_ADVERTISING_INTERVAL = 2000
BLE_SCAN_LENGTH = 5000
BLE_INTERVAL = 30000
BLE_WINDOW = 30000

# state variables
message_count = 0

def encode_message(message):
    """ Encode a message to bytes """
    return message.encode('utf-8')

def decode_message(message):
    """ Decode a message from bytes """
    return message.decode('utf-8')

async def blink_led_task():
    global connected
    toggle = True
    while True:
        led.value(toggle)
        toggle = not toggle
        blink = 1000 if connected else 250
        await asyncio.sleep_ms(blink)
        
async def receive_data_task(characteristic):
    """ Receive data from the connected device """
    global message_count
    while True:
        try:
            data = await characteristic.read()

            if data:
                print(f"{IAM} received: {decode_message(data)}, count: {message_count}")
                #await characteristic.write(encode_message("Got it"))
                

            message_count += 1
            await asyncio.sleep(0.1)

        except asyncio.TimeoutError:
            print("Timeout waiting for data in {ble_name}.")
            break
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

async def ble_scan():
    """ Scan for a BLE device with the matching service UUID """

    print(f"Scanning for BLE Beacon named {IAM_SENDING_TO}...")

    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            print(result)
            if result.name() == IAM_SENDING_TO and BLE_SVC_UUID in result.services():
                print(f"found {result.name()} with service uuid {BLE_SVC_UUID}")
                return result
    return None

async def run_central_mode():
    """ Run the central mode """
    global connected
    print("looking for UUID", BLE_SVC_UUID)
    # Start scanning for a device with the matching service UUID
    while True:
        device = await ble_scan()

        if device is None:
            continue
        print(f"device is: {device}, name is {device.name()}")

        try:
            print(f"Connecting to {device.name()}")
            connection = await device.device.connect()

        except asyncio.TimeoutError:
            print("Timeout during connection")
            continue

        print(f"{IAM} connected to {connection}")

        # Discover services
        async with connection:
            try:
                service = await connection.service(BLE_SVC_UUID)
                characteristic = await service.characteristic(BLE_CHARACTERISTIC_UUID)
                connected = True
            except (asyncio.TimeoutError, AttributeError):
                print("Timed out discovering services/characteristics")
                continue
            except Exception as e:
                print(f"Error discovering services {e}")
                await connection.disconnect()
                continue

            tasks = [
                asyncio.create_task(receive_data_task(characteristic)),
                asyncio.create_task(blink_led_task())
            ]
            await asyncio.gather(*tasks)
            connected = False

            await connection.disconnected()
            print(f"{BLE_NAME} disconnected from {device.name()}")
            break


asyncio.run(run_central_mode())


