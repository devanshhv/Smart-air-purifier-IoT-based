# Smart-air-purifier-IoT-based
Raspberry Pi Air Quality Monitor This project uses a Raspberry Pi in conjunction with multiple sensors to measure environmental air quality. The data from the DHT11 (temperature and humidity), SDS011 (PM2.5 and PM10 particulate matter), and MQ135 (CO₂ concentration) sensors are sent to the Blynk IoT platform for real-time monitoring via a mobile app.

Features Real-time monitoring of temperature, humidity, PM2.5, PM10, and CO₂ concentration.

Data from sensors is sent to Blynk for remote monitoring and visualization on a mobile app.

Continuous data updates every 5 seconds for accurate tracking.

Supports MQ135 sensor calibration for estimating CO₂ levels in parts per million (ppm).

Hardware Requirements Raspberry Pi (any model with GPIO pins and I²C support)

DHT11 sensor for temperature and humidity

SDS011 sensor for particulate matter (PM2.5 and PM10)

MQ135 sensor for air quality (CO₂ estimation)

ADS1115 ADC for reading analog signals from MQ135

I²C and Serial communication interfaces

Blynk account and Auth Token

Software Requirements Python 3.x

Required libraries:

adafruit_dht (for DHT11)

adafruit_ads1x15 (for ADS1115 ADC)

BlynkLib (for communication with Blynk)

pyserial (for serial communication with SDS011)

busio (for I²C communication)

Installation Set up the Raspberry Pi:

Install the necessary libraries:

bash Copy Edit pip install adafruit-circuitpython-dht adafruit-circuitpython-ads1x15 BlynkLib pyserial Enable I²C and Serial on the Raspberry Pi using raspi-config.

Connect the sensors:

DHT11: Connect to a GPIO pin (e.g., GPIO17).

SDS011: Connect via USB to the Raspberry Pi (Serial communication).

MQ135: Connect the analog output to the ADS1115 ADC, which is connected via I²C to the Raspberry Pi.

Set up Blynk:

Create a Blynk account and get an Auth Token.

Replace the BLYNK_AUTH variable in the script with your own token.

Run the script:

Execute the Python script on the Raspberry Pi:

bash Copy Edit python air_quality_monitor.py Usage The data from all sensors will be sent to Blynk every 5 seconds.

You can view the real-time values of temperature, humidity, PM2.5, PM10, and CO₂ concentration on the Blynk mobile app using widgets that correspond to virtual pins V0, V1, V2, V3, V4, and V5.

Calibration The MQ135 sensor requires calibration in a clean air environment to get accurate CO₂ readings.

The code uses a calibration voltage value for clean air (CLEAN_AIR_VOLTAGE), which can be adjusted based on your environment.

License This project is open-source and released under the MIT License.
