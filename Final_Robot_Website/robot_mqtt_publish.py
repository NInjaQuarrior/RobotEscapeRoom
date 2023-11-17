"""
    File Created By: Liang Lu, Zachary Sarrett 
    File Created On: Mar. 20, 2023 
    Description: 
        this files stores the paho mqtt client publisher
        https://pypi.org/project/paho-mqtt/ 
        some examples we can use: 
            https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4
            https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
"""
from time import sleep
import paho.mqtt.client as mqtt
# pi_ip_address = '130.215.122.93'
pi_ip_address = 'mqtt.eclipseprojects.io'


def connect_mqtt() -> mqtt:
    # def on_connect(client, userdata, flags, rc):
    #     print(f"Connected with result code {rc}")

    client = mqtt.Client(client_id="robot_escape_pub", clean_session=True)
    # client.on_connect = on_connect
    client.connect(pi_ip_address)
    return client


def publish(client, topic):
    msg_count = 1
    while True:
        # msg = f"message: \"{msg_count}\""
        result = client.publish(topic, payload=msg_count)
        status = result[0]
        if status == 0:
            print(f"{msg_count} sent to topic {topic}")
        else:
            print(f"Failed to send message with status {status}")
        msg_count += 1
        sleep(10)

def publishMessage(client, topic, message):
    # msg = f"message: \"{msg_count}\""
    result = client.publish(topic, payload=message.encode('utf-8'))
    result.wait_for_publish()
    status = result[0]
    if status == 0:
        print(f"{message} sent to topic {topic}")
    else:
        print(f"Failed to send message with status {status}")


def mqtt_pub():
    client = connect_mqtt()
    client.loop_start()
    publish(client, "room/puzzle")


if __name__ == '__main__':     # Program start from here
    mqtt_pub()
