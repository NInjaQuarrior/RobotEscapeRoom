Client = None

class Response(object):
    completed = False
    topic = ""      #string
    trigger = []    #list of strings
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

def makeResponse(topic, trigger, responses):
    response = Response(topic, trigger, responses)
    return response

def responseChoice(type, value):
    match type:
        case "publish":     # value = [topic, value]
            Client.publish(value[0], payload=value[1])
            return
        case "log":         # value: string
            print(value)
            return
        case "unsubscribe": # value: string
            Client.unsubscribe(value)
            return
        case _:
            print('bad response')
            return

#1: tests recieving
#2 tests multiple completion conditions
#3 tests a response publishing a message (also multiple responses)
#4 tests unsubscribing by then calling for a fail case
testList = [makeResponse("test", ["1"], [["log", "test 1 succeeded"]]), 
              makeResponse("test", ["-1"], [["log", "testing failed"]]), 
              makeResponse("test", ["1", "10"], [["log", "test 2 succeeded"]]),
              makeResponse("test", ["10"], [["log", "publishing \"13\" to test"], ["publish", ["test", 13]]]),
              makeResponse("test", ["13"], [["log", "test 3 succeeded"]]),
              makeResponse("test", ["13"], [["unsubscribe", "test"], ["publish", ["test", -1]], ["log", "test 4 succeeded"]])
              ]

def processSubscriptionsTest(client, userdata, msg):
    print("recieved message | topic: "+msg.topic +
          " \tmsg: "+str(msg.payload.decode("utf-8")))
    for response in testList:
        if(not(response.completed) and response.topic == msg.topic):
            response.respond(str(msg.payload.decode("utf-8")))
    return

def testMQTT(client):
    global Client
    Client = client
    print('testing')
    Client.on_message = processSubscriptionsTest
    sub = Client.subscribe("test")
    if(sub[1]==128):
        print('subscribing failed')
        return -1
    print('subscribed')
    result1 = Client.publish("test", payload=1)
    if(result1[1]==128):
        print('publishing failed')
        return -1
    result2 = Client.publish("test", payload=1)
    if(result2[1]==128):
        print('publishing failed')
        return -1
    result3 = Client.publish("test", payload=10)
    if(result3[1]==128):
        print('publishing failed')
        return -1
    print('published')

# "simultaneous" responses (same completion conditions) go in order as listed here
puzzleList = []
# template: makeResponse("", [""], [["", ]])

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