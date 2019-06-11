import json
import random
from utils.dht11 import DHT11

class BaseSensor():
	def __init__(self, sensor_id):
		self.type = 'dummysensor'
		self.sensor_id = sensor_id
		self.current_measure = 0.0
		return
		
	@property
	def state(self):
		return {
			"sensor_id" : self.sensor_id,
			"measure" : self.current_measure
		}
		
	def store_current_raw_signal(self):
		if random.random() > 0.5:
			self.current_measure += random.random()
		else:
			self.current_measure -= random.random()

	def read(self):
		self.store_current_raw_signal()
		print(self.type + ' new measure: ' + str(self.current_measure))
		return self.current_measure		


class TemperatureSensor(BaseSensor):
	def __init__(self, sensor_id):
		BaseSensor.__init__(self, sensor_id)
		self.type = 'temperature'
		self.physical_sensor = DHT11()
		return
		
	@property
	def state(self):
		return {
			"sensor_id" : self.sensor_id,
			"measure" : self.current_measure
		}
		
	def read(self):
		self.current_measure = float(self.physical_sensor.collect())
		print(self.type + ' new measure: ' + str(self.current_measure))
		return self.current_measure		


	