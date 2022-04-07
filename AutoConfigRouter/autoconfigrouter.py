from logging import exception
from fireREST import FMC
from AutoConfigRouter import CONNECTION_ERROR, CREDENTIAL_ERROR, SESSION_ERROR
import requests

#client = request.session()

def addRulesCisco(ruleset, login, passwd, ip_addr):
    fmc = FMC(ip_addr,login,passwd,"Global")
    for x in ruleset:
        rule = {
            'interface': x[0],
            'action': x[1],
            'source': x[2],
            'user': x[3],
            'securitygroup': x[4],
            'destination' : x[5],
            'securitygroup': x[6],
            'service': x[7],
            'description': x[8],
            'logging': x[9],
            'logginglevel': x[10],
        }
        fmc.policy.accesspolicy.create(data=rule)

def getRulesCisco(login, passwd, ip_addr):
    fmc = FMC(ip_addr, login, passwd,"Global")
    print(fmc.policy.accesspolicy.get())            


def getRulesFortigate(url, api_key):
    try:
        #Policies request
        url_cust_req="http://"+url+"/api/v2/cmdb/firewall/policy?access_token="+api_key
        r = requests.get(url=url_cust_req, headers="Authorization: Bearer "+api_key, verify=False)
        
        if(r == None):
            raise Exception
        else:
            print(r)
    except Exception:
        return SESSION_ERROR
    