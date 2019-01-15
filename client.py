import paho.mqtt.client as paho
import time
import json
from datetime import datetime
import MySQLdb as mdb
import threading

ClientID = "Client1"

MQTTServer= "mqttlocalserver.local"
MQTTPort= 1883
username = "debian"
password = "temppwd"

LastWillTopic = "LWT"
LastWillMessage = ClientID
OutMessageTopic = "OUT/"+ClientID
InMessageTopic = "IN/"+ClientID

db_hostname = "localhost"
db_database = "MQTTData"
db_username = "debian"
db_password = "temppwd"

class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

def on_publish(client, userdata, mid):
    pass
def on_connect(client, userdata, flags, rc):
    if(rc==0):
        mqttclient.subscribe(InMessageTopic)
def on_message(client, userdata, msg):
    msg.payload=eval(msg.payload)
    if(msg.topic==InMessageTopic):
        try:
            x.execute("""DELETE FROM Data WHERE TimeStamp="""+"\""+str(msg.payload["TimeStamp"])+"\"")
            conn.commit()
        except Exception,e:
            print str(e)
            conn.rollback()

def sendStored():
    try:
        x.execute("select * from Data")
        records = x.fetchall()
        for row in records:
            mqttclient.publish(OutMessageTopic, str(row[1]), qos=1)
    except:
        conn.rollback()

def storeData(data):
    ts = time.time()
    data["TimeStamp"] =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data["ClientID"] = ClientID
    mqttclient.publish(OutMessageTopic,str(data))
    try:
        x.execute("""INSERT into Data (TimeStamp,Data) values(%s,%s)""",(data["TimeStamp"],str(data)))
        conn.commit()
    except:
        conn.rollback()

conn = mdb.connect(host=db_hostname,user=db_username,passwd=db_password,db=db_database)
x = conn.cursor()
mqttclient = paho.Client()
mqttclient.username_pw_set(username,password)
mqttclient.will_set(LastWillTopic,LastWillMessage,qos=1,retain=False)
mqttclient.on_publish = on_publish
mqttclient.on_connect = on_connect
mqttclient.on_message = on_message
mqttclient.connect(MQTTServer,MQTTPort)
mqttclient.loop_start()
setInterval(30,sendStored)
