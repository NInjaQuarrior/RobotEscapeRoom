from time import sleep
Client = None

class Response(object):
	completed = False
	topic = ""	  #string
	trigger = []	#list of strings
	responses = []   # [string type, list(string)/string values (see responseChoice)]

	def __init__(self, topic, trigger, responses):
		self.topic = topic
		self.trigger = trigger
		self.responses = responses
	
	def respond(self, value):
		if(value in self.trigger):
			self.trigger[self.trigger.index(value)] = True
			for trigger in self.trigger:
				if(not(trigger == True)):
					return
			for response in self.responses:
				responseChoice(response[0], response[1])
			self.completed = True
			#responseChoice("unsubscribe", self.topic)

def makeResponse(topic, trigger, responses):
	response = Response(topic, trigger, responses)
	return response

def responseChoice(type, value):
	match type:
		case "publish":	 # value = [topic, value]
			Client.publish(value[0], payload=value[1])
			return
		case "log":		 # value: string
			print(value)
			return
		case "unsubscribe": # value: string
			Client.unsubscribe(value)
			return
		case _:
			print('bad response')
			return

puzzleList = [ makeResponse("setup", ["start"], [["publish", ["room/setup/cabinet_1", "0,0"]], ["publish", ["room/cabinet_1", "CLOSE"]], ["publish", ["room/setup/door_1", "1,0"]]]),
	makeResponse("node3", ["switch_1"], [["publish", ["node1", "node3"]], ["publish", ["node7", "node3"]]]),
	makeResponse("room/switch_1", ["True"], [["publish", ["node3", "switch_1"]]]),
	makeResponse("node1", ["node3"], [["publish", ["room/cabinet_1", "OPEN"]]]),
	makeResponse("node7", ["node3"], [["publish", ["room/door_1", "open,0,0"]]])]

def processSubscriptions(client, userdata, msg):
	print("recieved message | topic: "+msg.topic +
		  " \tmsg: "+str(msg.payload.decode("utf-8")))
	for response in puzzleList:
		if(not(response.completed) and response.topic == msg.topic):
			response.respond(str(msg.payload.decode("utf-8")))
	return

def runMQTT(client):
	global Client
	Client = client
	Client.on_message = processSubscriptions
	topics = []
	for response in puzzleList:
		if not(response.topic in topics):
			topics.append(response.topic)
	for topic in topics:
		sub = Client.subscribe(topic)
		if(sub[1]==128):
			print('Failed to subscribe to topics')
	Client.publish("setup", payload = "start")
	sleep(1.0)