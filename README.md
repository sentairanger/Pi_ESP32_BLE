# Pi_ESP32_BLE
This project allows you to communicate between a Raspberry Pi and ESP32 using BLE. I will accompany this project with a Medium article soon.

* `ble_esp32.py`: This will run on your ESP32 to connect to the Pi.
* `esp32_correct`: This will run on your Pi to connect to the ESP32. No the file name is not wrong. I chose that file name because I was distinguishing it from the old versions of the file I was working on.
* `find_mac.py`: This will find the MAC address of your ESP32.
* The `esp_pi_dual` directory contains the `esp32_two_way` code that is used on the Pi to send and receive data to and from the ESP32 and the `ble_two_way.py` code is used on the ESP32 to send and receive data to and from the Pi.
* The `esp32_pi_pot`directory contains the `ble_pot.py` code that is used on the ESP32 to send values of the potentiometer to the Pi, the `esp32_connect.py` code that receives potentiometer values from the ESP32 and the `esp32_pot.py` code changes the brightness of the LED depending on the potentiometer level.
* The `esp32_pi_button` folder contains the `ble_button.py` code that is used to send data to the Pi (0 for pressed, 1 for released), the `esp32_connect.py` code that the Pi uses to receive data from the ESP32 and the `esp32_button.py` code that turns the LED on the Pi when the data is 1 and off when the data is 0.

Click on this [link](https://medium.com/@ed2point0/how-i-got-my-raspberry-pi-and-esp32-to-talk-to-each-other-3cb2cd95ccc2) for the write up on this project.

* Initial setup
![Picture](https://github.com/sentairanger/Pi_ESP32_BLE/blob/main/esp32-pi_bb.jpg)

* Setup with Potentiometer
![Picture](https://github.com/sentairanger/Pi_ESP32_BLE/blob/main/esp32-pi-pot_bb.jpg)

* Setup with Potentiometer and LED
![LED](https://github.com/sentairanger/Pi_ESP32_BLE/blob/main/esp32-pi-pot2_bb.jpg)

* Setup with Button and LED
![Button](https://github.com/sentairanger/Pi_ESP32_BLE/blob/main/esp32-pi-button_bb.jpg)
