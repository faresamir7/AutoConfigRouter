from asyncio.windows_events import NULL
from logging import exception
from fireREST import FMC

from AutoConfigRouter import CONNECTION_ERROR

fmc = FMC("192.168.1.1","cisco","cisco","Global")

def getRule():
    try:
        if(fmc!=NULL):
            ruleset = fmc.policy.accesspolicy.get()
            print(ruleset)
        else:
            raise Exception
    except Exception:
        return CONNECTION_ERROR
            

def addRule(rule):
    try:
        if(fmc!=NULL):
            print(fmc.policy.accesspolicy.create(rule))
        else:
            raise Exception
    except Exception:
        return CONNECTION_ERROR
