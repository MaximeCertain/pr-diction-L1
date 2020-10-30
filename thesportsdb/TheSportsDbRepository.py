import requests
from thesportsdb.StaticInfos import StaticInfos

def getNextRound():
    next = requests.get("https://www.thesportsdb.com/api/v1/json/1/eventsnextleague.php?id=4334")
    return next.json()["events"]

def getEventRoundForLigue(ligueId, roundId):
    r = requests.get(url='https://www.thesportsdb.com/api/v1/json/1/eventsround.php?id=%d&r=%d&s=%s' % (ligueId, roundId, StaticInfos.currentSeasonYears))
    return r.json()["events"]

    #retourne prochain id de journée
def getNextRoundId():
    events = getNextRound()
    return int(events[0]["intRound"]) + 1

def getLastMatchsForTeam(teamId):
    r = requests.get(url='https://www.thesportsdb.com/api/v1/json/1/eventslast.php?id=%d' % (int(teamId)))
    return r.json()["results"]
