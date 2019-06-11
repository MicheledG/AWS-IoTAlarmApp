import time
from utils.device import Device
from utils.config import MQTT_IDENTITY


def main():
	device = Device(MQTT_IDENTITY)
	while True:
		try:	
			time.sleep(2)
			device.publish_state()
		except KeyboardInterrupt:
			device.destroy()
			break
		except Exception as e:
			print(str(e))
			print('Unknown error, restarting..')
			device = Device(MQTT_IDENTITY)


if __name__ == "__main__":
	main()
