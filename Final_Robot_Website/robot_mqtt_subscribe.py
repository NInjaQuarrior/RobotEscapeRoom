"""
    File Created By: Liang Lu, Zachary Sarrett 
    File Created On: Mar. 20, 2023 
    Description: 
        this files stores the paho mqtt client subscriber
        https://pypi.org/project/paho-mqtt/ 
        some examples we can use: 
            https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4
            https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
"""
from time import sleep
import paho.mqtt.client as mqtt
# pi_ip_address = '130.215.122.93'
pi_ip_address = "mqtt.eclipseprojects.io"


def connect_mqtt() -> mqtt:
    # def on_connect(client, userdata, flags, rc):
    #     print(f"Connected with result code {rc}")

    client = mqtt.Client(client_id="robot_escape_sub", clean_session=True)
    # client.on_connect = on_connect
    client.connect(pi_ip_address)
    return client


def subscribe(client: mqtt, topic):
    def on_message(client, userdata, msg):
        print("on_message | topic: "+msg.topic +
              " \tmsg: "+str(msg.payload.decode("utf-8")))

    client.subscribe(topic)
    client.on_message = on_message


def mqtt_sub():
    client = connect_mqtt()
    subscribe(client, "robot/test")
    subscribe(client, "robot/aruco")
    subscribe(client, "robot/function")
    subscribe(client, "robot/puzzle")
    subscribe(client, "website/test")
    subscribe(client, "website/status")
    subscribe(client, "room/test")
    subscribe(client, "room/puzzle")
    client.loop_forever()


if __name__ == '__main__':     # Program start from here
    mqtt_sub()
