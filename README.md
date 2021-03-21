# IoTHealthStation
Code that accompanies an AWS blog post showing how a builder can connect a Raspberry Pi hosted sensor (max30102) in this case to the cloud to be processed. Please see this post: ___ for more information!

# Bill of Materials:
* Raspberry Pi WH
* SSD1306 Screen
* MAX30102 Sensor
* DHT11 Sensor
* Breadboard and dupont cables 

# Wiring Diagram:
![iothealthstation_bb](https://user-images.githubusercontent.com/54914619/111858884-ad9b8800-8912-11eb-9c6d-63eeef2785d5.png)

# Wiring Schematic:
![iothealthstation_schem](https://user-images.githubusercontent.com/54914619/111858892-c2781b80-8912-11eb-8ca5-b71e1629df9b.png)

# Files Within:
* [`mqtt.py`](raspberry_pi/mqtt.py) sends MQTT to AWS IoT Core using connection parms set in iothealthstation.py
* [`iothealthstation.py`](raspberry_pi/iothealthstation.py) main entry point on Raspberry Pi (use python3)
* [`heartrate_monitor.py`](raspberry_pi/heartrate_monitor.py) this file computes the heartrate from the sensor library

# Libraries Used:
* [https://github.com/doug-burrell/max30102](https://github.com/doug-burrell/max30102)
* [https://github.com/Pithikos/python-websocket-server](https://github.com/Pithikos/python-websocket-server)

# Punch List
- iothealthstation.py None type error handling or approach on if is none
- button/light logic
- add print connect to message
- deal with sequence
- parameterize connect into config file (look at piot)
