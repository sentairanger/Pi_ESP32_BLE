# import libraries
from micropython import const
import asyncio
import struct
import aioble
import bluetooth
from esp32 import raw_temperature
from machine import Pin

# Define variables
led = Pin(2, Pin.OUT)
connected = False

_BLE_SERVICE_UUID = bluetooth.UUID('19b10000-e8f2-537e-4f6c-d104768a1214')
_BLE_READ_CHAR_UUID = bluetooth.UUID('19b10001-e8f2-537e-4f6c-d104768a1214')
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
        message = f"Temperature: {raw_temperature()}"
        #print(message)
        try:
            msg = encode_message(message)
            read_characteristic.write(msg)
            await asyncio.sleep(1)
        except Exception as ex:
            print(f"Error: {ex}")
            continue

# Run as peripheral
async def run_peripheral_mode():
    global connected
    print("ESP32 starting to advertise")
    while True:
        try:
            async with await aioble.advertise(
                _ADV_INTERVAL_MS, name="ESP32", services=[_BLE_SERVICE_UUID],) as connection:
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
    
    
    
            
