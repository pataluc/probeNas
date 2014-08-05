#!/usr/bin/python
#   Title: probeNas.py
#   Author: Chopper_Rob
#   Date: 05-08-2014
#   Info: get infos from nas and store them in domoticz
 
import sys
import datetime
import time
import os
import subprocess
import urllib2
import json
 
# Settings for the domoticz server
domoticzserver="127.0.0.1:8080"
nasip="172.22.29.20"
community="public"

nas_switch_idx=""

nas_temps='{"snmpPrefix": "1.3.6.1.4.1.6574.2.1.1.6.%s", "drives":[{"id": "0", "idx": ""}]}'
nas_spaces='{"snmpPrefix": "1.3.6.1.2.1.25.2.3.1.%s.%s", "volumes":[{"id": "36", "idx": "29"}]}'


def 
 
print "exit" 
sys.exit(0)
 
device=sys.argv[1]
switchid=sys.argv[2]
interval=sys.argv[3]
cooldownperiod=sys.argv[4]
previousstate=-1
lastsuccess=datetime.datetime.now()
lastreported=-1
domoticzurl = 'http://'+domoticzserver+'/json.htm?type=devices&filter=all&used=true&order=Name'
 
if int(subprocess.check_output('ps x | grep \'' + sys.argv[0] + ' ' + sys.argv[1] + '\' | grep -cv grep', shell=True)) > 2 :
 print datetime.datetime.now().strftime("%H:%M:%S") + "- script already running. exiting."
 sys.exit(0)
 
def domoticzstatus ():
  request = urllib2.Request(domoticzurl)
  response = urllib2.urlopen(request)
 
  json_object = json.loads(response.read())
 
  if json_object["status"] == "OK":
    for i, v in enumerate(json_object["result"]):
      if json_object["result"][i]["idx"] == switchid and "Lighting" in json_object["result"][i]["Type"] :
        if json_object["result"][i]["Status"] == "On":
          status = 1
        if json_object["result"][i]["Status"] == "Off":
          status = 0
  return status
 
print datetime.datetime.now().strftime("%H:%M:%S") + "- script started."
 
lastreported = domoticzstatus()
if lastreported == 1 :
  print datetime.datetime.now().strftime("%H:%M:%S") + "- according to domoticz, " + device + " is online"
if lastreported == 0 :
  print datetime.datetime.now().strftime("%H:%M:%S") + "- according to domoticz, " + device + " is offline"
 
while 1==1:
  currentstate = subprocess.call('ping -q -c1 -W 1 '+ device + ' > /dev/null', shell=True)
 
  if currentstate == 0 : lastsuccess=datetime.datetime.now()
  if currentstate == 0 and currentstate != previousstate and lastreported == 1 :
    print datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + " online, no need to tell domoticz"
  if currentstate == 0 and currentstate != previousstate and lastreported != 1 :
    if domoticzstatus() == 0 :
      print datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + " online, tell domoticz it's back"
      urllib2.urlopen("http://" + domoticzserver + "/json.htm?type=command&param=switchlight&idx=" + switchid + "&switchcmd=On&level=0")
    else:
      print datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + " online, but domoticz already knew" 
    lastreported=1
 
  if currentstate == 1 and currentstate != previousstate :
    print datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + " offline, waiting for it to come back"
 
  if currentstate == 1 and (datetime.datetime.now()-lastsuccess).total_seconds() > float(cooldownperiod) and lastreported != 0 :
    if domoticzstatus() == 1 :
      print datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + " offline, tell domoticz it's gone"
      urllib2.urlopen("http://" + domoticzserver + "/json.htm?type=command&param=switchlight&idx=" + switchid + "&switchcmd=Off&level=0")
    else:
      print datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + " offline, but domoticz already knew"
    lastreported=0
 
  time.sleep (float(interval))
 
  previousstate=currentstate
