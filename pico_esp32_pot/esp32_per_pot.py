# import libraries
from micropython import const
import asyncio
import struct
import aioble
import bluetooth
from esp32 import raw_temperature
from machine import Pin
import json

with open("uuids.json", mode="r", encoding="utf-8") as read_file:
    uuids_data = json.load(read_file) 

# Define variables
led = Pin(2, Pin.OUT)
pot = ADC(Pin(13))
pot.atten(ADC.ATTN_11DB)
connected = False

_BLE_SERVICE_UUID = bluetooth.UUID(uuids_data["service"])
_BLE_READ_CHAR_UUID = bluetooth.UUID(uuids_data["characteristic"])
_BLE_WRITE_UUID = bluetooth.UUID('19b10002-e8f2-537e-4f6c-d104768a1214')

_ADV_INTERVAL_MS = 250_000

# Define our characteristics and services
ble_service = aioble.Service(_BLE_SERVICE_UUID)
read_characteristic = aioble.Characteristic(ble_service, _BLE_READ_CHAR_UUID, read=True, notify=True)
write_characteristic = aioble.Characteristic(ble_service, _BLE_WRITE_UUID, read=True, write=True, notify=True, capture=True)

aioble.register_services(ble_service)

# encode and decode messages
def encode_message(message):
    """Encode a message to bytes."""
    return message.encode('utf-8')

def decode_message(message):
    """Decode a message from bytes."""
    return message.decode('utf-8')

# Blink LED when connected to Pi
async def blink_led_task():
    global connected
    toggle = True
    while True:
        led.value(toggle)
        toggle = not toggle
        blink = 1000 if connected else 250
        await asyncio.sleep_ms(blink)

# Send data to Pi
async def send_data_task(connection, read_characteristic):
    while True:
        pot_value = pot.read() 
        message = pot_value
        #print(message)
        try:
            msg = encode_message(message)
            read_characteristic.write(msg)
            await asyncio.sleep(0.1)
        except Exception as ex:
            print(f"Error: {ex}")
            continue
        
# Run as peripheral
async def run_peripheral_mode():
    global connected
    print("ESP32 advertising with UUID:", _BLE_SERVICE_UUID)
    while True:
        try:
            async with await aioble.advertise(
                _ADV_INTERVAL_MS, name="Peripheral", services=[_BLE_SERVICE_UUID],) as connection:
                connected = True
                print("Connection from", connection.device)
                tasks = [
                        asyncio.create_task(send_data_task(connection, read_characteristic)),
                        asyncio.create_task(blink_led_task())
                    ]
                await asyncio.gather(*tasks)
                await connection.disconnected()
                connected = False
        except asyncio.CancelledError:
            # Catch the CancelledError
            print("Peripheral task cancelled")
        except Exception as e:
            print("Error in peripheral_task:", e)
        finally:
            # Ensure the loop continues to the next iteration
            await asyncio.sleep_ms(100)


asyncio.run(run_peripheral_mode())
    
    
    
            
