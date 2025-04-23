import time
import board
import adafruit_dht
import serial
from BlynkLib import Blynk

from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1115 as ADS
import busio
import math

# Blynk Auth Token
BLYNK_AUTH = 'Z3_xlD-FAVig-559mbx7Vy43amGbJZld'

# Setup Blynk
blynk = Blynk(BLYNK_AUTH)

# DHT11 Setup
dhtDevice = adafruit_dht.DHT11(board.D17)

# SDS011 Setup
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=2)

# MQ135 via ADS1115 Setup
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
mq135_channel = AnalogIn(ads, ADS.P0)  # Connected to A0

# Calibration value: voltage output of MQ135 in clean air
CLEAN_AIR_VOLTAGE = 1.4  # Adjust this based on your real environment

def voltage_to_ppm(voltage, clean_air_voltage=CLEAN_AIR_VOLTAGE):
    try:
        rs = (5.0 - voltage) / voltage
        ro = (5.0 - clean_air_voltage) / clean_air_voltage
        ratio = rs / ro
        ppm = 116.6020682 * math.pow(ratio, -2.769034857)
        return ppm
    except ZeroDivisionError:
        return None

def read_sds011():
    data = ser.read(10)
    if len(data) >= 10 and data[0] == 0xAA and data[1] == 0xC0:
        pm25 = (data[3] * 256 + data[2]) / 10.0
        pm10 = (data[5] * 256 + data[4]) / 10.0
        return pm25, pm10
    return None, None

print("Sending data to Blynk... Press Ctrl+C to stop.")
try:
    while True:
        blynk.run()

        # DHT11 Reading
        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            if temperature is not None and humidity is not None:
                print(f"DHT11 - Temp: {temperature}°C, Humidity: {humidity}%")
                blynk.virtual_write(0, temperature)
                blynk.virtual_write(1, humidity)
        except RuntimeError as e:
            print(f"DHT11 Error: {e.args[0]}")

        # SDS011 Reading
        pm25, pm10 = read_sds011()
        if pm25 is not None:
            print(f"SDS011 - PM2.5: {pm25} µg/m³, PM10: {pm10} µg/m³")
            blynk.virtual_write(2, pm25)
            blynk.virtual_write(3, pm10)

        # MQ135 Reading
        mq135_voltage = mq135_channel.voltage
        mq135_ppm = voltage_to_ppm(mq135_voltage)

        print(f"MQ135 - Voltage: {mq135_voltage:.3f} V, CO₂: {mq135_ppm:.1f} ppm")
        blynk.virtual_write(4, mq135_voltage)  # V4 = voltage
        if mq135_ppm is not None:
            blynk.virtual_write(5, round(mq135_ppm, 1))  # V5 = CO2 ppm

        time.sleep(5)

except KeyboardInterrupt:
    print("Stopped by user. Exiting...")
    ser.close()
    dhtDevice.exit()