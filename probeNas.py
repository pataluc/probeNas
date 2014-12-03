#!/usr/bin/python
#   coding=UTF-8
#
#   Title: probeNas.py
#   Author: Luc Fouin <luc.fouin@gmail.com>
#   Date: 03/12/2014
#   Info: get infos from nas and store them in domoticz
 
from pysnmp.entity.rfc3413.oneliner import cmdgen
import urllib2
 
# Settings for the domoticz server
domoticzserver = '127.0.0.1:8080'
nas_ip = '172.22.29.20'
#nas_ip = '10.8.2.30'
nas_snmp_port = 161
community = 'public'

nas_switch_idx = 37

nas_temp_snmpprefix = "1.3.6.1.4.1.6574.2.1.1.6.%s"
nas_temp_drives = [
        {'id': 0, 'idx': 30}, # id: SNMP id of the drive, idx: domoticz id of the temperature probe
        {'id': 1, 'idx': 31},
        {'id': 2, 'idx': 32},
        {'id': 3, 'idx': 33},
        {'id': 4, 'idx': 34}
    ]

nas_space_snmpprefix = "1.3.6.1.2.1.25.2.3.1.%s.%s"
nas_space_volumes = [
        {'id': 39, 'idx': 29}, # id: SNMP id of the volume, idx: domoticz id of the percentage probe
        {'id': 38, 'idx': 35}
    ]

#TODO: ping server with sthing like :  subprocess.check_call(['ping','-c1',ip])

oids = []

for drive in nas_temp_drives :
    oids.append(nas_temp_snmpprefix % drive['id'])

for volume in nas_space_volumes : 
    for i in [5, 6] :
        oids.append(nas_space_snmpprefix % (i, volume['id']))

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(cmdgen.CommunityData(community), cmdgen.UdpTransportTarget((nas_ip, nas_snmp_port)), *oids)
if errorIndication:
    print(errorIndication)
elif errorStatus:
    print(errorStatus)

results = {}

# result transcoding, from list to dict
for name, val in varBinds:
    results[name.prettyPrint()] = val

# send values to domoticz for drives temperatures
for drive in nas_temp_drives :
    #    http://$DOMO_IP:$DOMO_PORT/json.htm?type=command&param=udevice&idx=$NAS_HD1_TEMP_IDX&nvalue=0&svalue=$HDtemp1
    snmp_id = nas_temp_snmpprefix % drive['id']
    url = "http://%s/json.htm?type=command&param=udevice&idx=%s&nvalue=0&svalue=%s" % (domoticzserver, drive['idx'], results[snmp_id])
    urllib2.urlopen(urllib2.Request(url))


# send values to domoticz for volume usage
for volume in nas_space_volumes :
    hd_total = results[nas_space_snmpprefix % (5, volume['id'])]
    hd_used = results[nas_space_snmpprefix % (6, volume['id'])]

    hd_free = 100 * float(hd_used) / float(hd_total)
    url = "http://%s/json.htm?type=command&param=udevice&idx=%s&nvalue=0&svalue=%s" % (domoticzserver, volume['idx'], hd_free)
    urllib2.urlopen(urllib2.Request(url))


