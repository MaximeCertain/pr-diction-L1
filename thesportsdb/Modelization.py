from thesportsdb.Cleaner import *
import pandas as pd

from thesportsdb.StaticInfos import StaticInfos
from thesportsdb.TheSportsDbRepository import getEventRoundForLigue, getNextRoundId

Last5MatchsForRound = []

###
def transformDataframe(lastEventsForTeam, idTeam):
    lastEventsForTeam["isHome"] = 0
    lastEventsForTeam["isWinning"] = 0
    lastEventsForTeam["isWinning"] = lastEventsForTeam["isHome"] = lastEventsForTeam["scoredGoals"] = lastEventsForTeam[
        "concededGoals"] = 0
    # victoire ou non
    lastEventsForTeam.loc[((lastEventsForTeam['intHomeScore'] > lastEventsForTeam["intAwayScore"]) & (
            lastEventsForTeam['idHomeTeam'] == str(idTeam)) | (
                                   lastEventsForTeam['intAwayScore'] > lastEventsForTeam["intHomeScore"]) & (
                                   lastEventsForTeam['idAwayTeam'] == str(idTeam))), 'isWinning'] = 1
    # domicile ou non
    lastEventsForTeam.loc[(lastEventsForTeam['idHomeTeam'] == str(idTeam)), 'isHome'] = 1
    # nb de buts de l'équipe sur un match
    lastEventsForTeam.loc[(lastEventsForTeam['idHomeTeam'] == str(idTeam)), 'scoredGoals'] = lastEventsForTeam[
        "intHomeScore"]
    lastEventsForTeam.loc[(lastEventsForTeam['idAwayTeam'] == str(idTeam)), 'scoredGoals'] = lastEventsForTeam[
        "intAwayScore"]
    lastEventsForTeam.loc[(lastEventsForTeam['idHomeTeam'] == str(idTeam)), 'concededGoals'] = lastEventsForTeam[
        "intAwayScore"]
    lastEventsForTeam.loc[(lastEventsForTeam['idAwayTeam'] == str(idTeam)), 'concededGoals'] = lastEventsForTeam[
        "intHomeScore"]

    lastEventsForTeam["nameTeam"] = lastEventsForTeam["strHomeTeam"]
    lastEventsForTeam["opponentNameTeam"] = lastEventsForTeam["strAwayTeam"]

    lastEventsForTeam.loc[(lastEventsForTeam['idAwayTeam'] == str(idTeam)), 'nameTeam'] = lastEventsForTeam[
        "strAwayTeam"]
    lastEventsForTeam.loc[(lastEventsForTeam['idAwayTeam'] == str(idTeam)), 'opponentNameTeam'] = lastEventsForTeam[
        "strHomeTeam"]

    return lastEventsForTeam

###Recupère les 5 derniers matchs d'une équipe
def getDataframe(idTeam):
    idRound = 8
    matchsForTeam = []
    for i in range(idRound - 1, idRound - 6, -1):
        pastMatchForTeam = getMatchForTeamInRound(int(idTeam), i)
        statsResults5MatchsAgo = getlast5MatchsStatsForTeam(idTeam, int(pastMatchForTeam["intRound"]))
        pastMatchForTeam["score5LastMatchs"] = statsResults5MatchsAgo["last5MatchsScores"]
        pastMatchForTeam["goalAverageLast5Matchs"] = statsResults5MatchsAgo["last5MatchsGoalAverage"]
        pastMatchForTeam["last5MatchsScoredGoals"] = statsResults5MatchsAgo["last5MatchsScoredGoals"]
        pastMatchForTeam["last5MatchsConcededGoals"] = statsResults5MatchsAgo["last5MatchsConcededGoals"]
        pastMatchForTeam["last5MatchsWins"] = statsResults5MatchsAgo["last5MatchsWins"]
        pastMatchForTeam["last5MatchsLoss"] = statsResults5MatchsAgo["last5MatchsLoss"]
        idOpponent = int(pastMatchForTeam["idAwayTeam"]) if int(pastMatchForTeam['idHomeTeam']) == int(idTeam) else int(
            pastMatchForTeam["idHomeTeam"])
        statsResuls5MatchsAgoForOpponent = getlast5MatchsStatsForTeam(idOpponent, int(pastMatchForTeam["intRound"]))
        pastMatchForTeam["opponentScore5LastMatchs"] = statsResuls5MatchsAgoForOpponent["last5MatchsScores"]
        pastMatchForTeam["opponentGoalAverageLast5Matchs"] = statsResuls5MatchsAgoForOpponent["last5MatchsGoalAverage"]
        pastMatchForTeam["opponentLast5MatchsScoredGoals"] = statsResuls5MatchsAgoForOpponent["last5MatchsScoredGoals"]
        pastMatchForTeam["opponentLast5MatchsConcededGoals"] = statsResuls5MatchsAgoForOpponent[
            "last5MatchsConcededGoals"]
        pastMatchForTeam["opponentLast5MatchsWins"] = statsResuls5MatchsAgoForOpponent["last5MatchsWins"]
        pastMatchForTeam["opponentLast5MatchsLoss"] = statsResuls5MatchsAgoForOpponent["last5MatchsLoss"]
        matchsForTeam.append(pastMatchForTeam)
    matchsForTeam = cleanEvents(pd.DataFrame(matchsForTeam))
    df = (transformDataframe(matchsForTeam, idTeam))

    return cleanPostTransformationEvent(df)


last5MatchsForRound = dict()

##charge les derniers matchs de Ligue 1 dans le dictionnaire last5MatchsForRound
def load5LastMatchs(idRound):
    if last5MatchsForRound == {}:
        # charge dataset
        for i in range(idRound - 1, idRound - 38, -1):
            if (i > 0 and i <= 38):
                matchs = getEventRoundForLigue(StaticInfos.ligue1Id, i)
                last5MatchsForRound[i] = matchs

##recupère u n match à partir du dictionnaire last5MatchsForRound
def getMatchForTeamInRound(idTeam, idRound):
    matchs = last5MatchsForRound[idRound]
    for match in matchs:
        if int(match['idHomeTeam']) == int(idTeam) or int(match["idAwayTeam"]) == int(idTeam):
            return match


# donne les statistiques d'une équipe sur les 5 derniers matchs par rapport au match qu'elle va jouer
def getlast5MatchsStatsForTeam(idTeam, roundId):
    last5MatchsScores = last5MatchsGoalAverage = concededGoals = scoredGoals = wins = loss = 0
    for i in range(roundId - 1, roundId - 6, -1):
        if i <= 0 or i > 38:
            continue
        pastMatchForTeam = getMatchForTeamInRound(int(idTeam), i)
        isHome = int(pastMatchForTeam['idHomeTeam']) == int(idTeam)
        draw = (int(pastMatchForTeam["intHomeScore"])) == int(pastMatchForTeam["intAwayScore"])
        if draw:
            last5MatchsScores += 1
        elif isHome:
            if (int(pastMatchForTeam["intHomeScore"])) > int(pastMatchForTeam["intAwayScore"]):
                last5MatchsScores += 3
                wins += 1
            else:
                loss += 1
        else:
            if int(pastMatchForTeam["intAwayScore"]) > int(pastMatchForTeam["intHomeScore"]):
                last5MatchsScores += 3
                wins += 1
            else:
                loss += 1

        if isHome:
            last5MatchsGoalAverage += int(pastMatchForTeam["intHomeScore"])
            last5MatchsGoalAverage -= int(pastMatchForTeam["intAwayScore"])
            concededGoals += int(pastMatchForTeam["intAwayScore"])
            scoredGoals += int(pastMatchForTeam["intHomeScore"])
        else:
            last5MatchsGoalAverage += int(pastMatchForTeam["intAwayScore"])
            last5MatchsGoalAverage -= int(pastMatchForTeam["intHomeScore"])
            concededGoals += int(pastMatchForTeam["intHomeScore"])
            scoredGoals += int(pastMatchForTeam["intAwayScore"])

    statsResults = {"last5MatchsScores": last5MatchsScores * 100 / 15, "last5MatchsGoalAverage": last5MatchsGoalAverage,
                    "last5MatchsScoredGoals": scoredGoals, "last5MatchsConcededGoals": concededGoals,
                    "last5MatchsWins": wins, "last5MatchsLoss": loss}

    return statsResults


# Forme un dataframe contenant les stats des 100 derniers matchs L1 afin de faire de la prédiction
def makeDataframeForRound(df):
    dfTotal = pd.DataFrame()
    for i in range(0, len(df)):
        match = df.iloc[i]
        awayDataframe = getDataframe(int(match['idAwayTeam']))
        homeDataframe = getDataframe(int(match['idHomeTeam']))
        if (dfTotal.empty):
            dfTotal = pd.concat([awayDataframe, homeDataframe])
        else:
            dfMatch = pd.concat([awayDataframe, homeDataframe])
            dfTotal = pd.concat([dfTotal, dfMatch])
    return dfTotal


#Construit un dataframe avec une seule ligne à partir de deux Id. Sert à faire de la prédiction sur la ligne retourné
def getNextMatchDataframe(idTeamHome, idOpponent, type="home"):
    roundId = getNextRoundId()-2
    load5LastMatchs(roundId)
    nextMatchForTeam = {}
    statsResults5MatchsAgo = getlast5MatchsStatsForTeam(idTeamHome, roundId)
    nextMatchForTeam["score5LastMatchs"] = statsResults5MatchsAgo["last5MatchsScores"]
    nextMatchForTeam["goalAverageLast5Matchs"] = statsResults5MatchsAgo["last5MatchsGoalAverage"]
    nextMatchForTeam["last5MatchsScoredGoals"] = statsResults5MatchsAgo["last5MatchsScoredGoals"]
    nextMatchForTeam["last5MatchsConcededGoals"] = statsResults5MatchsAgo["last5MatchsConcededGoals"]
    nextMatchForTeam["last5MatchsWins"] = statsResults5MatchsAgo["last5MatchsWins"]
    nextMatchForTeam["last5MatchsLoss"] = statsResults5MatchsAgo["last5MatchsLoss"]

    statsResuls5MatchsAgoForOpponent = getlast5MatchsStatsForTeam(idOpponent, roundId)

    nextMatchForTeam["opponentScore5LastMatchs"] = statsResuls5MatchsAgoForOpponent["last5MatchsScores"]
    nextMatchForTeam["opponentGoalAverageLast5Matchs"] = statsResuls5MatchsAgoForOpponent["last5MatchsGoalAverage"]
    nextMatchForTeam["opponentLast5MatchsScoredGoals"] = statsResuls5MatchsAgoForOpponent["last5MatchsScoredGoals"]
    nextMatchForTeam["opponentLast5MatchsConcededGoals"] = statsResuls5MatchsAgoForOpponent["last5MatchsConcededGoals"]
    nextMatchForTeam["opponentLast5MatchsWins"] = statsResuls5MatchsAgoForOpponent["last5MatchsWins"]
    nextMatchForTeam["opponentLast5MatchsLoss"] = statsResuls5MatchsAgoForOpponent["last5MatchsLoss"]
    matchsForTeam = cleanEvents(pd.DataFrame([nextMatchForTeam]))
    matchsForTeam = cleanPostTransformationEvent(matchsForTeam)

    matchsForTeam['isHome'] = 1 if type == "home" else 0

    return matchsForTeam
