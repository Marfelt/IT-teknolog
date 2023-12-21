from mpu6050 import mpu6050
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Create an MPU6050 object
sensor = mpu6050(0x68)  # The default I2C address for MPU6050 is 0x68

# Set up GPIO for the buzzer
buzzer_pin = 18  # Adjust this to the GPIO pin connected to the buzzer
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Set up PWM for the buzzer
pwm = GPIO.PWM(buzzer_pin, 1000)  # 1000 Hz frequency, you can adjust it
pwm.start(0)  # Start with 0% duty cycle

# MQTT settings
mqtt_broker_address = "192.168.233.93"
mqtt_topic = "test/topic"

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Message Published")

def beep_twice():
    for _ in range(2):
        pwm.ChangeDutyCycle(50)  # Adjust duty cycle for desired volume
        time.sleep(0.2)
        pwm.ChangeDutyCycle(0)
        time.sleep(0.1)

def has_fallen():
    status = False

    # Set up MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Connect to the MQTT broker
    client.connect(mqtt_broker_address, 1883, 60)
    client.loop_start()

    while True:
        # Read acceleration data
        acceleration = sensor.get_accel_data()

        # Extract acceleration values
        acceleration_x = acceleration['x']
        acceleration_y = acceleration['y']
        acceleration_z = acceleration['z']

        print(f"Acceleration x: {acceleration_x}, y: {acceleration_y}, z: {acceleration_z}")
        time.sleep(0.2)

        # Check for a fall event
        if acceleration_z > 8 and not status:
            print("A person has fallen!")
            status = True

            # Publish message to MQTT topic
            fall_message = "Person has fallen!"
            client.publish(mqtt_topic, fall_message)

            # Trigger the buzzer with a higher-pitched sound
            beep_twice()

        if acceleration_x > 8 and not status:
            print("A person has fallen!")
            status = True

            # Publish message to MQTT topic
            fall_message = "Person has fallen!"
            client.publish(mqtt_topic, fall_message)

            # Trigger the buzzer with a higher-pitched sound
            beep_twice()

        # Add similar checks for other axes

        if acceleration_y > 8 and status:
            status = False

        time.sleep(2)

if __name__ == "__main__":
    try:
        has_fallen()
    finally:
        pwm.stop()  # Stop PWM on program exit
        GPIO.cleanup()  # Cleanup GPIO on program exit
