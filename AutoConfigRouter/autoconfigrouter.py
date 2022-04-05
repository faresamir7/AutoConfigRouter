from logging import exception
from fireREST import FMC
from AutoConfigRouter import CONNECTION_ERROR, CREDENTIAL_ERROR, SESSION_ERROR

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
        addRuleCisco(rule)


def getRuleCisco(fmc):
    try:
        if(fmc!=None):
            ruleset = fmc.policy.accesspolicy.get()
            print(ruleset)
        else:
            raise Exception
    except Exception:
        return CONNECTION_ERROR
            

def addRuleCisco(rule,fmc):
    try:
        if(fmc!=None):
            print(fmc.policy.accesspolicy.create(rule))
        else:
            raise Exception
    except Exception:
        return CONNECTION_ERROR


def getRulesFortigate(headers, url, customerID):
    try:
        #Policies request
        url_cust_req=url+"/customers/"+customerID+"/policyobjects"
        r = client.get(url_cust_req, headers=headers, verify=False)
        
        if(r == None):
            raise Exception
        else:
            print(r)
    except Exception:
        return SESSION_ERROR
    