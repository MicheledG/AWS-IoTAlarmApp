#!/usr/bin/python
import RPi.GPIO as GPIO
import time

class DHT11():

    def __init__(self):
        self.channel = 7
        return

    def collect(self):
        while True:
            data = []
            GPIO.setmode(GPIO.BOARD)
            time.sleep(2)
            GPIO.setup(self.channel, GPIO.OUT)
            GPIO.output(self.channel, GPIO.LOW)
            time.sleep(0.02)
            GPIO.output(self.channel, GPIO.HIGH)
            GPIO.setup(self.channel, GPIO.IN)
            while GPIO.input(self.channel) == GPIO.LOW:
                continue
            while GPIO.input(self.channel) == GPIO.HIGH:
                continue
            j = 0
            while j < 40:
                k = 0
                while GPIO.input(self.channel) == GPIO.LOW:
                    continue
                while GPIO.input(self.channel) == GPIO.HIGH:
                    k += 1
                    if k > 100:
                        break
                if k < 8:
                    data.append(0)
                else:
                    data.append(1)
                j += 1

            # print("sensor is working.")
            # print(data)
            humidity_bit = data[0:8]
            humidity_point_bit = data[8:16]
            temperature_bit = data[16:24]
            temperature_point_bit = data[24:32]
            check_bit = data[32:40]
            humidity = 0
            humidity_point = 0
            temperature = 0
            temperature_point = 0
            check = 0
            for i in range(8):
                humidity += humidity_bit[i] * 2 ** (7 - i)
                humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
                temperature += temperature_bit[i] * 2 ** (7 - i)
                temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
                check += check_bit[i] * 2 ** (7 - i)
            tmp = humidity + humidity_point + temperature + temperature_point
            if check == tmp:
                #print "temperature:%d.%d" %(temperature,temperature_point),"C"," humidity :", humidity, "%"
                temp_string = "%d.%d" %(temperature,temperature_point)
                #print temp_string
                return float(temp_string)
            else:
                #print("Temperature sensor invalid measure! Retrying...")
                #print(temperature)
                time.sleep(0.5)
                #return self.collect()

