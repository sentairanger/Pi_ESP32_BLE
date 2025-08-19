# Pi_ESP32_BLE
This project allows you to communicate between a Raspberry Pi and ESP32 using BLE. I will accompany this project with a Medium article soon.

* `ble_esp32.py`: This will run on your ESP32 to connect to the Pi.
* `esp32_correct`: This will run on your Pi to connect to the ESP32. No the file name is not wrong. I chose that file name because I was distinguishing it from the old versions of the file I was working on.
* `find_mac.py`: This will find the MAC address of your ESP32.
* The `esp_pi_dual` directory contains the `esp32_two_way` code that is used on the Pi to send and receive data to and from the ESP32 and the `ble_two_way.py` code is used on the ESP32 to send and receive data to and from the Pi. 

Click on this [link](https://medium.com/@ed2point0/how-i-got-my-raspberry-pi-and-esp32-to-talk-to-each-other-3cb2cd95ccc2) for the write up on this project.

![Picture](https://github.com/sentairanger/Pi_ESP32_BLE/blob/main/esp32-pi_bb.jpg)
