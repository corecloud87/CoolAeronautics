import paho.mqtt.client as mqtt
import jwt
import requests

# Configuration
device_id = "device1"
password = "password123"
auth_url = "http://localhost:5000/login"
mqtt_broker = "localhost"
mqtt_topic = "aeronautics/data"

# Authenticate and get JWT token
response = requests.post(auth_url, json={'device_id': device_id, 'password': password})
token = response.json().get('token')

if not token:
    print("Authentication failed")
    exit()

# JWT Verification function for MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    try:
        payload = jwt.decode(msg.payload, "your_secret_key", algorithms=["HS256"])
        print(f"Received message: {payload}")
    except jwt.ExpiredSignatureError:
        print("Token expired")
    except jwt.InvalidTokenError:
        print("Invalid token")

# MQTT Client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Set JWT token as will message
client.will_set(mqtt_topic, jwt.encode({'message': 'Disconnected', 'device_id': device_id}, "your_secret_key", algorithm="HS256"))

client.connect(mqtt_broker, 1883, 60)
client.loop_start()

# Publish message with JWT
message = jwt.encode({'data': 'sensor_data', 'device_id': device_id}, "your_secret_key", algorithm="HS256")
client.publish(mqtt_topic, message)

client.loop_forever()
