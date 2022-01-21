from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
import random
import json
import datetime as datetime

def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

host = "a290uc2ksy4m1j-ats.iot.us-west-2.amazonaws.com"

rootCAPath = "D:/SmartGarden/Huy/garden/smartgarden/rootca.pem"
certificatePath = "D:/SmartGarden/Huy/garden/smartgarden/certificate.pem.crt"
privateKeyPath = "D:/SmartGarden/Huy/garden/smartgarden/private.pem.key"

my_rpi = AWSIoTMQTTClient("basicPubSub")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
my_rpi.connect()
my_rpi.subscribe("smartgarden/tests", 1, customCallback)

# Publish to the same topic in a loop forever
while True:
	sleep(4)
	test1 = random.randint(1, 10)
	test2 = random.randint(1, 10)
	test3 = random.randint(1, 10)
	test4 = random.randint(1, 10)
	test5 = random.randint(1, 10)
	test6 = random.randint(1, 10)

	message = {}
	message["id"] = "id_smartgarden"

	now = datetime.datetime.now()
	message["datetimeid"] = now.isoformat()
	message["test1"] = test1
	message["test2"] = test2
	message["test3"] = test3
	message["test4"] = test4
	message["test5"] = test5
	message["test6"] = test6

	my_rpi.publish("smartgarden/tests", json.dumps(message), 1)
