import threading
from time import sleep
import paho.mqtt.client as mqtt
import GPS
from imu import has_fallen

# Create an MQTT client
mqtt_client = mqtt.Client()


# MQTT settings
mqtt_broker_address = "192.168.233.93"
mqtt_topic = "test/topic"

# Connect to the MQTT broker
mqtt_client.connect(mqtt_broker_address, 1883, 60)
mqtt_client.loop_start()
ser =  GPS.port_setup()

def gps_loop():
    while True:
        try:
            gps_coords = GPS.parseGPSdata(ser)

            if gps_coords is None or gps_coords[0] == 0.0:
                print("No Data")
            else:
                latitude, longitude = gps_coords
                print(f"{latitude}, {longitude}")

                # Construct a message with the GPS coordinates
                message = f"{latitude}, {longitude}"

                # Publish message to MQTT topic
                mqtt_client.publish(mqtt_topic, message)
            sleep(5)

        except KeyboardInterrupt as e:
            print("--- GPS Loop shutting down ---")
            break

def imu_loop():
    while True:
        try:
            # Your IMU logic here
            has_fallen()
            sleep(1)

        except KeyboardInterrupt as e:
            print("--- IMU Loop shutting down ---")
            break

# Create threads for GPS and IMU loops
gps_thread = threading.Thread(target=gps_loop)
imu_thread = threading.Thread(target=imu_loop)

# Start both threads
gps_thread.start()
imu_thread.start()


# Wait for both threads to finish
gps_thread.join()
imu_thread.join()
