from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import datetime
import sys


class HealthMQTT:
    "Common base class for all employees"

    def __init__(self, deviceid, host, topic):
        self.deviceid = deviceid
        self.clientid = deviceid
        self.host = host
        self.topic = topic
        self.sleep_time = 1
        certPath = "certs/{}/".format(deviceid)

        # Init AWSIoTMQTTClient
        self.myAWSIoTMQTTClient = None
        self.myAWSIoTMQTTClient = AWSIoTMQTTClient(self.clientid)
        self.myAWSIoTMQTTClient.configureEndpoint(host, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(
            "{}AmazonRootCA1.pem".format(certPath),
            "{}private.pem.key".format(certPath),
            "{}certificate.pem.crt".format(certPath),
        )

        # AWSIoTMQTTClient connection configuration
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        self.myAWSIoTMQTTClient.connect()

    def sendmsg(self, message):
        message["sequence"] = 12  # loopCount change this
        message["timestamp"] = int(datetime.datetime.now().timestamp() * 1000)

        messageJson = json.dumps(message)
        repeat = 0
        while True:
            try:
                self.myAWSIoTMQTTClient.publish(self.topic, messageJson, 1)
                print("published", message["sequence"])
                break
            except:
                if repeat > 10:
                    print("bailing out after 10 attempts")
                    sys.exit(1)
                repeat += 1
                print("retrying, error occured while send MQQT")
                time.sleep(2)

    def disconnect(self):
        self.myAWSIoTMQTTClient.disconnect()