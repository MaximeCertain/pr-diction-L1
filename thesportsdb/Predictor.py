import pickle

from thesportsdb.Modelization import getNextMatchDataframe

#à partir de deux Identifiants, retourne un tableau de deux entiers avec la probabilité pour chaque équipe d'obtenir la victoire
def getPredictionsResult(idTeamA, idTeamB):
    results = {}
    results[idTeamA] = predictWinnerInOpposition(idTeamA, idTeamB, type="home")
    results[idTeamB] = predictWinnerInOpposition(idTeamB, idTeamA, type="away")
    return results

#prédit pour une équipe
def predictWinnerInOpposition(idTeamA, idTeamB, type="home"):
    opposition = getNextMatchDataframe(idTeamA, idTeamB, type)
    score = predictNextVictoryForTeam(opposition)
    victoryPredictionPercentage = (round(score, 2) * 100)
    return victoryPredictionPercentage

###prédit le pourcentage de victoire selon le modèle enregistré sur kaagle
def predictNextVictoryForTeam(predicter):
    cls = pickle.load(open("L1_predict.pkl", "rb"))
    x_predictor = predicter[
        ['isHome', 'last5MatchsWins', 'last5MatchsLoss', 'opponentGoalAverageLast5Matchs',
         'last5MatchsConcededGoals', 'opponentLast5MatchsLoss', 'opponentLast5MatchsWins',
         'opponentLast5MatchsConcededGoals', 'opponentLast5MatchsScoredGoals',
         'last5MatchsScoredGoals', 'score5LastMatchs', 'goalAverageLast5Matchs', 'opponentScore5LastMatchs']]
    y = (cls.predict_proba(x_predictor)).max()

    return y
