# coding=utf-8
import time
from utils.mqtt_client import mqtt_client
from utils.relay import relay


def main():
	"""
	It executes the following main steps:
	- start the relay
	- connect the mqtt client
	- subscribe the message handler function on the notifications topic
	- wait for messages until a keyboard interrupt is provided

	:return:
	"""
	# 1. Start the relay
	relay.start()

	# 2. Initialize mqtt client
	mqtt_client.connect()

	# 3. Subscribe message handler function
	mqtt_client.subscribe(message_handler)

	# 4. Wait for messages
	try:
		while True:
			time.sleep(5)
	except KeyboardInterrupt:
		# Disconnect the mqtt client
		mqtt_client.unsubscribe()
		mqtt_client.disconnect()
		# Shutdown the relay component
		relay.shutdown()


def message_handler(payload):
	"""
	It receives messages produced by IoT Events detector model.

	It must switch on the relay if the danger status is reached and switch off the
	relay when danger status is exited (an other status is entered).

	:param payload: a dictionary with the following structure
	{
		"deviceId": "<device_id>",
		"eventName": "EnteredComfort|EnteredWarning|EnteredDanger",
		"temperature": <transition_temperature>
	}
	:type payload: dict
	:return:
	"""
	device_id = payload['deviceId']
	event_name = payload['eventName']
	if event_name == 'EnteredDanger':
		print "{device_id} in Danger status".format(device_id=device_id)
		relay.switch_on()
	elif event_name == 'EnteredComfort':
		print "{device_id} in Comfort status".format(device_id=device_id)
		relay.switch_off()
	else:
		print "{device_id} has generated an event of type {event_name} that is out of scope".format(
			device_id=device_id,
			event_name=event_name,
		)


if __name__ == "__main__":
	main()
