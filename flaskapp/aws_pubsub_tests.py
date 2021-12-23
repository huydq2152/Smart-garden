# # Import SDK packages
# from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
# from time import sleep
#
# def customCallback(client, userdata, message):
#     print("Received a new message: ")
#     print(message.payload)
#     print("from topic: ")
#     print(message.topic)
#     print("--------------\n\n")
#
#
# host = "a290uc2ksy4m1j-ats.iot.us-west-2.amazonaws.com"
#
# rootCAPath = "rootca.pem"
# certificatePath = "certificate.pem.crt"
# privateKeyPath = "private.pem.key"
#
# my_rpi = AWSIoTMQTTClient("basicPubSub")
# my_rpi.configureEndpoint(host, 8883)
# my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
#
# my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
# my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
# my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
# my_rpi.configureMQTTOperationTimeout(5)  # 5 sec
#
# # Connect and subscribe to AWS IoT
# my_rpi.connect()
# my_rpi.subscribe("smartgarden/tests", 1, customCallback)
#
# # Publish to the same topic in a loop forever
# loopCount = 0
# while True:
#     test1 = float(ser.readline())
#     test2 = float(ser.readline())
#     test3 = int(ser.readline())
#     test4 = int(ser.readline())
#
#     loopCount = loopCount + 1
#     message = {}
#     message["id"] = "id_smartgarden"
#     import datetime as datetime
#
#     now = datetime.datetime.now()
#     message["datetimeid"] = now.isoformat()
#     message["temperature"] = test1
#     message["humidity"] = test2
#     message["moisture"] = test3
#     message["light"] = test4
#     import json
#
#     my_rpi.publish("smartgarden/readings", json.dumps(message),
#                    1)  # Chuyển object nhận được thành dạng json và đẩy lên kênh smartgarden/readings
#
# # Có thể viết các hàm tự rend ra các thuộc tính và gửi lên hoặc có thể viết thêm hàm pubsub để tạo bảng khác