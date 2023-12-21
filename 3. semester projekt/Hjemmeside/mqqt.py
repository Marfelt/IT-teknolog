import paho.mqtt.client as mqtt
import sqlite3
import besked

mqtt_broker_host = "192.168.233.219"
mqtt_broker_port = 1883
sensor_topic = "forwarded_data"
db_file = 'fald_loc.db'

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

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(sensor_topic)

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"Received message on topic '{msg.topic}': {payload}")
    
    if payload == "Person1 has fallen!":
        besked.send_sms()
    
    elif payload != "Person has fallen!":
        with sqlite3.connect(db_file) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO fald_loc (topic, payload) VALUES (?, ?)', (msg.topic, payload))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error inserting into database: {e}")

    
pc_client = mqtt.Client()
pc_client.connect(mqtt_broker_host, mqtt_broker_port, 60)

pc_client.on_connect = on_connect
pc_client.on_message = on_message

pc_client.loop_forever()
