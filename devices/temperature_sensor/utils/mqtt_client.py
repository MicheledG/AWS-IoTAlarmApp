from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient, AWSIoTMQTTClient
import json
import config
import requests


class MqttClient(object):

	PUB_TOPIC = config.PUB_TOPIC

	# Set ThingsBoard host to "demo.thingsboard.io" or "localhost"
	THINGSBOARD_HOST = config.THINGSBOARD_HOST
	# Replace YOUR_ACCESS_TOKEN with one from Device details panel.
	ACCESS_TOKEN = config.ACCESS_TOKEN

	def __init__(self):
	
		# initialize clients
		self.myMQTTClient = AWSIoTMQTTClient(config.MQTT_IDENTITY)
		
		# For TLS mutual authentication
		self.myMQTTClient.configureEndpoint(config.MQTT_ENDPOINT, config.MQTT_PORT)
		self.myMQTTClient.configureCredentials(config.CAFILE, config.KEYFILE, config.CERTFILE)
		self.myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
		self.myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
		self.myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
		self.myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
		self.connect()
		return

	def connect(self):
		print "Connecting to cloud..."
		self.myMQTTClient.connect()
		print "Connection established"
			
	def publish(self, payload):
		# print 'Publishing message on {}'.format(self.PUB_TOPIC)
		try:
			self.myMQTTClient.publish(self.PUB_TOPIC, json.dumps(payload), 1)
		except Exception:
			print('Error during publish, measure lost. Reconnecting...')
			self.connect()
		sens_dict = {
			"temperature": payload['sensorData']['temperature']
		}
		headers = {'content-type': 'application/json'}
		r = requests.post(
			"http://{url}/api/v1/{token}/telemetry".format(
				url=self.THINGSBOARD_HOST,
				token=self.ACCESS_TOKEN
			),
			data=json.dumps(sens_dict),
			headers=headers
		)
		r.raise_for_status()
	
	def disconnect(self):
		print "Disconnecting from the cloud..."
		self.myMQTTClient.disconnect()

