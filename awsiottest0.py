# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
#from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
#import random, time
import logging
import time
import argparse
import json

# A random programmatic shadow client ID.
IoT_CLIENT = "CMPE181testClient"

# The unique hostname that &IoT; generated for
# this device.
HOST_NAME = "a1ybe0ucsqzgz5-ats.iot.us-west-1.amazonaws.com"

# The relative path to the correct root CA file for &IoT;,
# which you have already saved onto this device.
ROOT_CA = "./certs/AmazonRootCA1.pem"

# The relative path to your private key file that
# &IoT; generated for this device, which you
# have already saved onto this device.
PRIVATE_KEY = "./certs/501da5aeec-private.pem.key"

# The relative path to your certificate file that
# &IoT; generated for this device, which you
# have already saved onto this device.
CERT_FILE = "./certs/501da5aeec-certificate.pem.crt"

# A programmatic shadow handler name prefix.
IoTThing_name = "CMPE181Sensor1"

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient(IoT_CLIENT)
# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
# Configurations
# For TLS mutual authentication
myMQTTClient.configureEndpoint(HOST_NAME, 8883)
# For Websocket
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
# For TLS mutual authentication with TLS ALPN extension
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
myMQTTClient.configureCredentials(ROOT_CA, PRIVATE_KEY, CERT_FILE)
# For Websocket, we only need to configure the root CA
# myMQTTClient.configureCredentials("YOUR/ROOT/CA/PATH")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()
topic_name = "CMPE181topic1"
myMQTTClient.subscribe(topic_name, 1, customCallback)

# Publish to the same topic in a loop forever
#myMQTTClient.publish("CMPE181topic1", "myPayload", 0)
loopCount = 0
while loopCount<10:
    message = {}
    message['message'] = "test message"
    message['sequence'] = loopCount
    messageJson = json.dumps(message)
    myMQTTClient.publish(topic_name, messageJson, 1)
    print('Published topic %s: %s\n' % (topic_name, messageJson))
    loopCount += 1
    time.sleep(1)

myMQTTClient.unsubscribe(topic_name)
myMQTTClient.disconnect()
