#!/usr/bin/python
#   coding=UTF-8
#
#   Title: pingDevices.py
#   Author: Luc Fouin <luc.fouin@gmail.com>
#   Date: 03/12/2014
#   Info: check listed devices against last updated time to send notification for abnormal quiet devices
 
from datetime import *
import os
import requests
import yaml

# Settings for the domoticz server
domoticzserver = '127.0.0.1:8080'

# URL of Free mobile SMS API
smsAPIUrl = 'https://smsapi.free-mobile.fr/sendmsg'

# get params from YAML file (name after this script .yaml)
params = yaml.load(open(os.path.splitext(__file__)[0] + '.yaml'))
smsAPIUser = params['smsAPIUser']
smsAPIPass = params['smsAPIPass']
devices = params['devices']

# function to send notification
def sendNotification(msg) :
    r = requests.get(smsAPIUrl, params={u'user': smsAPIUser, u'pass': smsAPIPass, u'msg': msg}, verify=False)

# for each device do check
for device in devices : 
    idx = device['idx']
    timeout = device['timeout']

    url = "http://%s/json.htm?type=devices&rid=%s&used=true" % (domoticzserver, idx)
    jsonData = requests.get(url).json
    
    diff = datetime.today() - datetime.strptime(jsonData['result'][0]['LastUpdate'], '%Y-%m-%d %H:%M:%S')

    if diff.total_seconds() > timeout * 60 :
        print u"Envoi notif, pas de réponse de la sonde %s depuis plus de %s minutes (%s)" % (jsonData['result'][0]['Name'], timeout, diff)
        sendNotification(u"DOMOTICZ: Pas de réponse de la sonde %s depuis plus de %s minutes (%s)" % (jsonData['result'][0]['Name'], timeout, diff))
    else :
        print u"derniÃ¨re rÃ©ponse de %s il y a %s (< au timeout de %s minutes)" % (jsonData['result'][0]['Name'], diff, timeout)


