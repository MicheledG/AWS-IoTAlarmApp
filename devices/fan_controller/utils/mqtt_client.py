from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import config
import json


class MqttClient(object):

	DEFAULT_SUBSCRIPTION_TOPIC = config.SUB_TOPIC

	def __init__(self, subscription_topic=DEFAULT_SUBSCRIPTION_TOPIC):
		"""
		It initializes the MQTT client.

		"""
		self.myMQTTClient = AWSIoTMQTTClient(config.MQTT_IDENTITY)
		
		# Setup TLS options
		self.myMQTTClient.configureEndpoint(config.MQTT_ENDPOINT, config.MQTT_PORT)
		self.myMQTTClient.configureCredentials(config.CAFILE, config.KEYFILE, config.CERTFILE)
		self.myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
		self.myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
		self.myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
		self.myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

		# Setup subscription topic
		self.subscription_topic = subscription_topic

	def connect(self):
		print "Connecting to cloud..."
		self.myMQTTClient.connect()
		print "Connected"

	def subscribe(self, message_handler_function):
		print "Subscribing mqtt client to " + self.subscription_topic
		decorated_message_handler = MqttClient._decorate_message_handler(message_handler_function)
		self.myMQTTClient.subscribe(self.subscription_topic, 1, decorated_message_handler)
		print "Subscribed"

	def unsubscribe(self):
		print "Unsubscribing mqtt client from " + self.subscription_topic
		self.myMQTTClient.unsubscribe(self.subscription_topic)
		print "Unsubscribed"

	def disconnect(self):
		print "Disconnecting from the cloud..."
		self.myMQTTClient.disconnect()
		print "Disconnected"

	@staticmethod
	def _decorate_message_handler(message_handler):
		"""
		It decorate the provided message handler function in order to support
		mqtt client interface.

		:param message_handler:
		:return decorated_message_handler: func
		"""
		def decorated_message_handler(client, userdata, message):
			"""
			It wraps the provided message handler providing to it only
			the message, already loaded from json string.

			:param client:
			:param userdata:
			:param message:
			:type message: object
			:return:
			"""
			payload = json.loads(message.payload)
			print "New message received:\n%s" % json.dumps(payload, indent=2)
			print "Invoking message handler: %s" % message_handler.__name__
			try:
				message_handler(payload)
			except Exception as e:
				print "Error during message handler execution"
			print "Message handler completes"

		return decorated_message_handler


mqtt_client = MqttClient()
