import client
import random

def generateRandomvalues():
    dict={}
    dict["ACActivePower"]=random.uniform(200.20, 900.45)
    dict["ACReactivePower"]=random.uniform(200.20, 900.45)
    dict["DCPower"]=random.uniform(200.20,300.45)
    dict["ACVR"]=random.uniform(220.20,240.45)
    dict["ACVY"]=random.uniform(220.20,240.45)
    dict["ACVB"]=random.uniform(220.20,240.45)
    dict["ACIR"]=random.uniform(2.20,2.45)
    dict["ACIY"]=random.uniform(2.20,2.45)
    dict["ACIB"]=random.uniform(2.20,2.45)
    dict["DCV"]=random.uniform(220.20,240.45)
    dict["DCI"]=random.uniform(2.20,2.45)
    dict["LoadStatus"]=format(random.getrandbits(19) + (1 << 20), '020b')
    dict["Load1P"]=random.uniform(20.20, 90.45)
    dict["Load2P"]=random.uniform(20.20, 90.45)
    dict["Load3P"]=random.uniform(20.20, 90.45)
    dict["Load4P"]=random.uniform(20.20, 90.45)
    dict["Load5P"]=random.uniform(20.20, 90.45)
    dict["Load6P"]=random.uniform(20.20, 90.45)
    dict["Load7P"]=random.uniform(20.20, 90.45)
    dict["Load8P"]=random.uniform(20.20, 90.45)
    dict["Load9P"]=random.uniform(20.20, 90.45)
    dict["Load10P"]=random.uniform(20.20, 90.45)
    dict["Load11P"]=random.uniform(20.20, 90.45)
    dict["Load12P"]=random.uniform(20.20, 90.45)
    dict["Load13P"]=random.uniform(20.20, 90.45)
    dict["Load14P"]=random.uniform(20.20, 90.45)
    dict["Load15P"]=random.uniform(20.20, 90.45)
    dict["Load16P"]=random.uniform(20.20, 90.45)
    dict["Load17P"]=random.uniform(20.20, 90.45)
    dict["Load18P"]=random.uniform(20.20, 90.45)
    dict["Load19P"]=random.uniform(20.20, 90.45)
    dict["Load20P"]=random.uniform(20.20, 90.45)
    return dict


client.setInterval(10,client.storeData(generateRandomvalues()))
