import paho.mqtt.client as mqtt

# MQTT broker information
broker_address = "localhost"  # You can replace this with your MQTT broker's address
port = 1883  # Default MQTT port

# Callback function when a message is received
def on_message(client, userdata, message):
    print(f"Received message on topic '{message.topic}': {message.payload.decode()}")

# Create an MQTT client
client = mqtt.Client("Subscriber")

# Set the callback function for when a message is received
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, port)

# Subscribe to the topic "sensors/test/value"
client.subscribe("telegraf/sensors/test/1")

# Start the MQTT loop to listen for messages
client.loop_start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    # Disconnect the client and exit gracefully when Ctrl+C is pressed
    client.disconnect()
    client.loop_stop()
