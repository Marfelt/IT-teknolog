import sqlite3
import paho.mqtt.client as mqtt

# SQLite Database Setup
db_file = 'fald_loc.db'

# Create a table to store locally received data
with sqlite3.connect(db_file) as conn:
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS fald_loc')

    cursor.execute('''
        CREATE TABLE fald_loc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            payload TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

# MQTT Broker Settings on Pi 2
mqtt_broker_host = "localhost"  # Pi 2's broker
mqtt_broker_port = 1883
sensor_topic = "test/topic"

# Create MQTT Client on Pi 2
pi2_client = mqtt.Client()
pi2_client.connect(mqtt_broker_host, mqtt_broker_port, 60)

pc_mqtt_broker_host = "192.168.233.219"
pc_mqtt_broker_port = 1883
pc_forwarded_topic = "forwarded_data"

pc_client = mqtt.Client()


pc_client.connect(pc_mqtt_broker_host, pc_mqtt_broker_port, 60)

def skipdb():
    print("Message is 'Person has fallen!', skipping database insertion.")
# MQTT Callbacks on Pi 2
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(sensor_topic)

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8").strip()
    print(f"Received message on topic '{msg.topic}': {payload}")

    if payload == "Person has fallen!":
        skipdb()
    
    elif payload != "Person has fallen!":
        with sqlite3.connect(db_file) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO fald_loc (topic, payload) VALUES (?, ?)', (msg.topic, payload))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error inserting into database: {e}")


    # Forward relevant data to the PC
    pc_client.publish(pc_forwarded_topic, payload)
    print("message published")


# Set callbacks
pi2_client.on_connect = on_connect
pi2_client.on_message = on_message


pi2_client.loop_forever()