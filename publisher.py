import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


class GenerateAWSClientConnection:
    """ This class generates a connection to AWS IoT hub and allows to publis or subscribe to a  topic

        E.g. of instantiation
        aws_connection = GenerateAWSClientConnection(
            "rpi-sensors-env/SCS/aws/certs/root-CA.crt",
            "rpi-sensors-env/SCS/aws/certs/PAI_sensing_station.private.key",
            "rpi-sensors-env/SCS/aws/certs/PAI_sensing_station.cert.pem"
        )

    """
    counter = 0

    def __init__(self, rootCAPath=None, privateKeyPath=None, certificatePath=None):
        clientId = "basicPubSub"
        host = "a3rub8i9d306dd-ats.iot.eu-west-1.amazonaws.com"
        port = 8883
        self.topic = "sdk/test/Python"  # this should be...
        self.rootCAPath = rootCAPath or "root-CA.crt"
        self.privateKeyPath = privateKeyPath or "PAI_sensing_station.private.key"
        self.certificatePath = certificatePath or "PAI_sensing_station.cert.pem"
        self.aws_mqtt_client = AWSIoTMQTTClient(clientId)
        self.aws_mqtt_client.configureEndpoint(host, port)
        self.aws_mqtt_client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
        self.is_connected = self.aws_mqtt_client.connect()

    def publish(self, message, topic):
        if self.is_connected:
            print(message)
            print(topic, self.topic)
            message = {}
            message['message'] = message or 'yolo'
            message['sequence'] = self.counter
            msg_json = json.dumps(message)
            topic = topic or self.topic
            result = self.aws_mqtt_client.publish(topic, msg_json, 1)
            self.counter += 1
            return True if result else False
        return "Not connected"
