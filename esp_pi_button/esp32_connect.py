# import libraries
import asyncio
from bleak import BleakClient 
from gpiozero import LED

# Define variables
connected = False   

led = LED(17)

# Change this to your MAC Address
esp_32 = "9C:9C:1F:E9:FF:C2"

TEMP_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"
SERVICE_UUID = "19b10000-e8f2-537e-4f6c-d104768a1214"

# Blink LED when Pi is connected
async def blink_task():
    global connected 
    print("blink task started")
    toggle = True 
    while True:
        if toggle:
            led.on() 
        else:
            led.off()
        toggle = not toggle 
        blink = 1000  if connected else 250
        await asyncio.sleep(blink / 1000)

# Pi receives data
async def receive_task(client):
    while True:
        try:
            response = await client.read_gatt_char(TEMP_UUID)
            print(f"ESP 32 message received: {response.decode('utf-8')}")
            await asyncio.sleep(0.1)
        except Exception as ex:
            print(f"Error: {ex}")
            break
            
# Connect to ESP32
async def connect_to_esp32(address):
    global connected
    print(f"Connecting to {address}")
    async with BleakClient(address) as client:
        connected = client.is_connected
        print(f"Connected: {connected}")
        tasks = [
        asyncio.create_task(receive_task(client)),
        asyncio.create_task(blink_task())
        ]
        await asyncio.gather(*tasks)
    connected = False

loop = asyncio.get_event_loop()
loop.run_until_complete(connect_to_esp32(esp_32))
