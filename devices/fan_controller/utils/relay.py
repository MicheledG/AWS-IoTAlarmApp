import RPi.GPIO as GPIO
import config


class Relay(object):

    DEFAULT_RELAY_PIN = config.RELAY_PIN

    def __init__(self, relay_pin=DEFAULT_RELAY_PIN):
        self.relay_pin = relay_pin

    def start(self):
        """
        It configures raspberry pi pins turning on the relay component.

        :return:
        """
        print "Starting relay..."
        GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
        GPIO.setup(self.relay_pin, GPIO.OUT)
        print "Started"

    def shutdown(self):
        """
        It shutdowns the relay component.

        :return:
        """
        print "Shutting down relay..."
        GPIO.output(self.relay_pin, GPIO.LOW)
        GPIO.cleanup()  # Release resource
        print "Shut down"

    def switch_on(self):
        """
        It switches the relay on.

        :return:
        """
        print "Switching relay on..."
        GPIO.output(self.relay_pin, GPIO.HIGH)
        print "Relay on"

    def switch_off(self):
        """
        It switches the relay off.

        :return:
        """
        print "Switching relay off..."
        GPIO.output(self.relay_pin, GPIO.LOW)
        print "Relay off"


relay = Relay()
