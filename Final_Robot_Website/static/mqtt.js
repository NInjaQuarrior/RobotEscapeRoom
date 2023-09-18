// Creating a new client instance 
clientID = "website-escape-room";
host = "mqtt.eclipseprojects.io";
port = 80;
client = new Paho.MQTT.Client(host, Number(port), clientID);


function startConnect() {
    client.onMessageArrived = onMessageArrived;
    client.connect({
        onSuccess: onConnect
    });
}

function onConnect() {
    client.subscribe("robot/test");
    client.subscribe("robot/aruco");
    console.log("successfully connected to topics.");
}

function onMessageArrived(msg) {
    console.log("OnMessageArrived: " + msg.payloadString + "\tfrom Topic: " + msg.destinationName);
    //alert(message.payloadString);
}

function publishMessage(topic, msg) {
    Message = new Paho.MQTT.Message(msg);
    Message.destinationName = topic;

    client.send(Message);
    console.log("topic: " + topic + "\tmsg: " + msg);
}
