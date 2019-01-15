import paho.mqtt.client as paho
import time
import json
from datetime import datetime
import MySQLdb as mdb
import threading

ServerID = "Server1"

MQTTServer1= "localhost"
MQTTPort1= 1883
username1 = "debian"
password1 = "temppwd"

MQTTServer2= "18.223.28.156"
MQTTPort2= 1883
username2 = "ubuntu"
password2 = "password"

LastWillTopic = "LWT"
LastWillMessage = ServerID
OutMessageTopic = "OUT/"+ServerID
InMessageTopic1 = "OUT/#"
InMessageTopic2 = "IN/"+ServerID

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
def on_connect1(client, userdata, flags, rc):
    if(rc==0):
        mqttclient1.subscribe(InMessageTopic1)
def on_connect2(client, userdata, flags, rc):
    if(rc==0):
        mqttclient2.subscribe(InMessageTopic2)

def on_message1(client, userdata, msg):
    msg.payload = eval(msg.payload)
    mqttclient1.publish("IN/"+msg.payload["ClientID"],str(msg.payload))
    msg.payload["ServerID"]=ServerID
    mqttclient2.publish(OutMessageTopic,str(msg.payload))
    try:
        x.execute("""INSERT into MQTTData (TimeStamp,ClientID,Data) values(%s,%s,%s)""",(msg.payload["TimeStamp"],msg.payload["ClientID"],str(msg.payload)))
        conn.commit()
    except Exception,e:
        print str(e)
        conn.rollback()
    try:
        print msg.payload["LoadStatus"]
        x.execute("""INSERT into MQTTDataExpanded (TimeStamp,ClientID,ACActivePower,ACReactivePower,DCPower,ACVR,ACVY,ACVB,ACIR,ACIY,ACIB,DCV,DCI,LoadStatus,Load1P,Load2P,Load3P,Load4P,Load5P,Load6P,Load7P,Load8P,Load9P,Load10P,Load11P,Load12P,Load13P,Load14P,Load15P,Load16P,Load17P,Load18P,Load19P,Load20P) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"""+"b'"+str(msg.payload["LoadStatus"])+"'"+""",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (msg.payload["TimeStamp"],msg.payload["ClientID"],msg.payload["ACActivePower"],msg.payload["ACReactivePower"],
        msg.payload["DCPower"],msg.payload["ACVR"],msg.payload["ACVY"],msg.payload["ACVB"],msg.payload["ACIR"],msg.payload["ACIY"],msg.payload["ACIB"],msg.payload["DCV"],msg.payload["DCI"],
        msg.payload["Load1P"],msg.payload["Load2P"],msg.payload["Load3P"],msg.payload["Load4P"],msg.payload["Load5P"],msg.payload["Load6P"],msg.payload["Load7P"],msg.payload["Load8P"],msg.payload["Load9P"],msg.payload["Load10P"],
        msg.payload["Load11P"],msg.payload["Load12P"],msg.payload["Load13P"],msg.payload["Load14P"],msg.payload["Load15P"],msg.payload["Load16P"],msg.payload["Load17P"],msg.payload["Load18P"],msg.payload["Load19P"],msg.payload["Load20P"]))
        conn.commit()
    except Exception,e:
        print str(e)
        conn.rollback()

def on_message2(client, userdata, msg):
    if(msg.topic == InMessageTopic2):
        print msg.payload
        msg.payload = eval(msg.payload)
        try:
            x.execute("DELETE FROM MQTTData WHERE TimeStamp =%s AND ClientID=%s ",(msg.payload['TimeStamp'],msg.payload['ClientID'] ))
            conn.commit()
        except:
            conn.rollback()

def sendStored():
    try:
        x.execute("select * from MQTTData")
        records = x.fetchall()
        for row in records:
            mqttclient2.publish(OutMessageTopic, str(row[2]), qos=1)
    except:
        conn.rollback()
def createClient(data):
    try:
        x.execute("""INSERT into MQTTClientData (ClientID,ClientName,ClientPassword,ClientMobile,Load1Name,Load2Name,Load3Name,Load4Name,Load5Name,Load6Name,Load7Name,Load8Name,Load9Name,Load10Name,Load11Name,Load12Name,Load13Name,Load14Name,Load15Name,Load16Name,Load17Name,Load18Name,Load19Name,Load20Name,Load1Priority,Load2Priority,Load3Priority,Load4Priority,Load5Priority,Load6Priority,Load7Priority,Load8Priority,Load9Priority,Load10Priority,Load11Priority,Load12Priority,Load13Priority,Load14Priority,Load15Priority,Load16Priority,Load17Priority,Load18Priority,Load19Priority,Load20Priority) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(data["ClientID"],data["ClientName"],data["ClientPassword"],data["ClientMobile"],
        data["Load1Name"],data["Load2Name"],data["Load3Name"],data["Load4Name"],data["Load5Name"],data["Load6Name"],data["Load7Name"],data["Load8Name"],data["Load9Name"],data["Load10Name"],data["Load11Name"],data["Load12Name"],data["Load13Name"],data["Load14Name"],
        data["Load15Name"],data["Load16Name"],data["Load17Name"],data["Load18Name"],data["Load19Name"],data["Load20Name"],data["Load1Priority"],data["Load2Priority"],data["Load3Priority"],data["Load4Priority"],data["Load5Priority"],data["Load6Priority"],data["Load7Priority"],data["Load8Priority"],
        data["Load9Priority"],data["Load10Priority"],data["Load11Priority"],data["Load12Priority"],data["Load13Priority"],data["Load14Priority"],data["Load15Priority"],data["Load16Priority"],data["Load17Priority"],data["Load18Priority"],data["Load19Priority"],data["Load20Priority"]))
        conn.commit()
    except Exception,e:
        print str(e)
        conn.rollback()

conn = mdb.connect(host=db_hostname,user=db_username,passwd=db_password,db=db_database)
x = conn.cursor()
mqttclient1 = paho.Client()
mqttclient1.username_pw_set(username1,password1)
mqttclient1.will_set(LastWillTopic,LastWillMessage,qos=1,retain=False)
mqttclient1.on_publish = on_publish
mqttclient1.on_connect = on_connect1
mqttclient1.on_message = on_message1
mqttclient1.connect(MQTTServer1,MQTTPort1)
mqttclient1.loop_start()
mqttclient2 = paho.Client()
mqttclient2.username_pw_set(username2,password2)
mqttclient2.will_set(LastWillTopic,LastWillMessage,qos=1,retain=False)
mqttclient2.on_publish = on_publish
mqttclient2.on_connect = on_connect2
mqttclient2.on_message = on_message2
mqttclient2.connect(MQTTServer2,MQTTPort2)
mqttclient2.loop_start()
setInterval(30,sendStored)
