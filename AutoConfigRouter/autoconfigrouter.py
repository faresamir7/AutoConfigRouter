from http import cookiejar
from logging import exception
from operator import indexOf
from textwrap import indent
from fireREST import FMC
from fireREST import exceptions
from pyfortiapi import FortiGate
from AutoConfigRouter import CONNECTION_ERROR, CREDENTIAL_ERROR, SESSION_ERROR
import requests
import json

#client = request.session()

def addRulesCisco(ruleset, login, passwd, ip_addr, containerName):
    fmc = FMC(ip_addr,login,passwd,"https")
    for x in ruleset:
        rule = {'id': [x[0]],
                "vlanTags": {x[1]},
                "logBegin": x[2],
                "logEnd": x[3],
                "logFiles": x[4],
                "sendEventsToFMC": x[5],
                "type": "AccessRule",
                "action": x[6],
                "name": x[7],
                "enabled": x[8],
                "sourceNetworks": x[9],
                "destinationNetworks": x[10],
                "sourcePorts": x[11],
                "destinationPorts": x[12]
                }
        if(x[0]=="None"):
            rule.pop("id")
        if(x[1]=="None"):
            rule.pop("vlanTags")
        if(x[2]=="None"):
            rule.pop("logBegin")
        if(x[3]=="None"):
            rule.pop("logEnd")
        if(x[4]=="None"):
            rule.pop("logFiles")
        if(x[5]=="None"):
            rule.pop("sendEventsToFMC")
        if(x[6]=="None"):
            rule.pop("action")
        if(x[7]=="None"):
            rule.pop("name")
        if(x[8]=="None"):
            rule.pop("enabled")
        if(x[9]=="None"):
            rule.pop("sourceZones")
        if(x[10]=="None"):
            rule.pop("destinationZones")
        if(x[11]=="None"):
            rule.pop("sourcePorts")
        if(x[12]=="None"):
            rule.pop("destinationPorts")
        networks = fmc.object.network.get()
        for i in x[9]:
            if((not(i in networks.values()))):
                print("Source Network not found...")
                addNetObjCisco(fmc,i)
            if((not(i in networks.values()))):
                print("Destination Network not found...")
                addNetObjCisco(fmc,i)
        fmc.policy.accesspolicy.accessrule.create(data=rule,container_name=containerName)


def addZoneCisco(fmc: FMC, name):
    print("Adding Zone with the name: "+ name)
    print("Description: ")
    desc = str(input())
    r=1
    while(r>0):
        print("Interface: ")
        inter = str(input())
        if(fmc.object.interface.get(name=inter)==[]):
            print("Interface not found... Abort?")
            r = str(input())
            if(r.upper() == "Y"):
                return
            else:
                r = 1
    print("Mode: ")
    mode = str(input())
    query = {'description': desc,
            'interfaces': inter,
            'mode': mode,
            'name': name,
            'type': 'securityzone'}
    fmc.object.securityzone.create(data=query)

def addNetObjCisco(fmc: FMC, name):
    print("Adding Network Object with the name: "+ name)
    print("Description: ")
    desc = str(input())
    print("Type (HOST/NETWORK/FQDN/RANGE): ")
    subType = str(input())
    print("Value (IP/IP with netmask/Domain Name/IP-IP): ")
    ipaddr = str(input())
    query = {"description": desc,
            "dnsResolution": "IPV4_ONLY",
            "name": name,
            "subType": subType,
            "type": "networkobject",
            "value": ipaddr}
    fmc.object.network.create(data=query)

def addUserCisco(userset, login, passwd, ip_addr):
    fmc = FMC(ip_addr,login,passwd,"https")
    for x in userset:
        user  = {'identitySourceId': x[0],
                'name': x[1],
                'newPassword': '',
                'password': x[2],
                'type': 'user',
                'userRole': x[3],
                'userServiceTypes': [x[4]]}
        fmc.object.realmuser.create(data=user)

def addFTDCisco(ftdSet, login, passwd, ip_addr):
    fmc = FMC(ip_addr,login,passwd,"https")
    for x in ftdSet:
        accessPolicy = fmc.policy.accesspolicy.get(name=x[5])
        licenceCaps = x[4].split()
        ftd  = {"name": x[0],
                "hostName": x[1],
                "regKey": x[2],
                "type": x[3],
                "license_caps": licenceCaps,
                "accessPolicy": {
                    "id": accessPolicy["id"],
                    "type": "AccessPolicy",
                    "name": x[5]
                    }
                }
        fmc.device.devicerecord.create(data=ftd)

def getRulesCisco(login, passwd, ip_addr):
    fmc = FMC(ip_addr, login, passwd, "https")
    data = fmc.policy.accesspolicy.get()[0]
    uuidString = data["rules"]["links"]["self"]
    print(json.dumps(fmc.policy.accesspolicy.accessrule.get(container_uuid=uuidString[uuidString.index("policies/")+9:uuidString.index("/accessrules")]),indent=4))

def getPolicyCisco(login, passwd, ip_addr, containerName):
    fmc = FMC(ip_addr, login, passwd, "https")
    try:
        print(json.dumps(fmc.policy.accesspolicy.get(name=containerName),indent=4))
        return True
    except exceptions.ResourceNotFoundError:
        print("Policy with the name '"+containerName+"' does not exist, please add it in the FMC.")
        return False
def getDevicesCisco(login, passwd, ip_addr):
    fmc = FMC(ip_addr, login, passwd, "https")
    print(json.dumps(fmc.device.devicerecord.get(),indent=4))

def getUsersCisco(login, passwd, ip_addr):
    fmc = FMC(ip_addr, login, passwd, "https")
    print(json.dumps(fmc.object.realmuser.get(),indent=4))      

def getRulesFortigate(login, password, ip_addr):
    device = FortiGate(ipaddr=ip_addr,username=login,password=password)
    print(device.get_firewall_policy())