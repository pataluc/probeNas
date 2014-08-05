#!/usr/bin/python
#   Title: probeNas.py
#   Author: Chopper_Rob
#   Date: 05-08-2014
#   Info: get infos from nas and store them in domoticz
 
from pysnmp.entity.rfc3413.oneliner import cmdgen
 
# Settings for the domoticz server
domoticzserver="127.0.0.1:8080"
#nas_ip="172.22.29.20"
nas_ip="10.8.2.20"
nas_snmp_port=161
community="public"

nas_switch_idx=""

nas_temp_snmpprefix= "1.3.6.1.4.1.6574.2.1.1.6.%s"
nas_temp_drives = [{'id': 0, 'idx': ''}, {'id': 1, 'idx': '11'}]

nas_space_snmpprefix = "1.3.6.1.2.1.25.2.3.1.%s.%s"
nas_space_volumes=[{"id": "36", "idx": "29"}]

oids = []


cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(cmdgen.CommunityData(community), cmdgen.UdpTransportTarget((nas_ip, nas_snmp_port)), oid)
    '1.3.6.1.2.1.1.6.0'
)


for drive in nas_temp_drives:
    print "Id du drive : %s" % drive['id']
    print "Id domoticz de la sonde : %s" % drive['idx']


 
