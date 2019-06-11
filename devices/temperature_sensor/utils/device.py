import json
import random
from utils.mqtt_client import MqttClient
from utils.sensors import BaseSensor, TemperatureSensor

class Device():

	def __init__(self, device_id):
		self.device_id = device_id
		self.sensors = list()
		self.init_sensors()
		self.mqtt = MqttClient()
		return
		
	@property
	def state(self):
		return {
			"deviceId" : str(self.device_id),
			"sensorData" : {
				'{}'.format(sensor.type): sensor.current_measure
				for sensor in self.sensors
			}
		}

	def register_sensor(self, sensor):
		self.sensors.append(sensor)
	
	def init_sensors(self):
		#s1 = BaseSensor(1)
		#self.register_sensor(s1)
		s2 = TemperatureSensor(2)
		self.register_sensor(s2)

	def publish_state(self):
		for sensor in self.sensors:
			sensor.read()
		self.mqtt.publish(self.state)

	def destroy(self):
		print "Interrupt received"
		self.mqtt.disconnect()

		# clean sensor if needed
		# ...

		print "Device shutdown complete"
		return

		