# MQTT client
CAFILE = "./certificates/AmazonRootCA1.pem"
CERTFILE = "./certificates/certificate.pem.crt"
KEYFILE = "./certificates/private.pem.key"
MQTT_ENDPOINT = "<AWS IoT MQTT Broker endpoint>"
MQTT_PORT = "8883"
MQTT_IDENTITY = "fan-controller"
SUB_TOPIC = 'xchange/notifications'

# RELAY
RELAY_PIN = 10
