from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
import random
import json
import datetime as datetime
import jsonconverter as jsonc

import dynamodb


def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


host = "a290uc2ksy4m1j-ats.iot.us-west-2.amazonaws.com"

rootCAPath = "/home/pi/Templates/Project/smartgarden/rootca.pem"
certificatePath = "/home/pi/Templates/Project/smartgarden/certificate.pem.crt"
privateKeyPath = "/home/pi/Templates/Project/smartgarden/private.pem.key"

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

# publish data
data = jsonc.data_to_json(dynamodb.get_deviceCount())
loaded_data = jsonc.json.loads(data)

deviceCountStr = loaded_data[0]['deviceCount']
deviceCount = int(deviceCountStr)
while True:
    sleep(4)

    message = {}
    message["id"] = "id_smartgarden"

    now = datetime.datetime.now()
    message["datetimeid"] = now.isoformat()

    i = 1
    while i <= deviceCount:
        test = random.randint(1, 10)
        message[f'test{i}'] = test
        i += 1

    my_rpi.publish("smartgarden/tests", json.dumps(message), 1)
