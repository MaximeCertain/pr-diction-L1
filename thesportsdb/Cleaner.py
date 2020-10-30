###Traite une première fois les données, en ne gardant que celles dont a besoin pour la transformation
def cleanEvents(df):
    return df[df.columns[df.columns.isin(
        ['strEvent', 'idHomeTeam', 'idAwayTeam', 'opponentLast5MatchsScoredGoals', 'opponentNameTeam',
         'opponentLast5MatchsWins', 'opponentLast5MatchsLoss', 'opponentLast5MatchsConcededGoals',
         'opponentScore5LastMatchs', 'opponentGoalAverageLast5Matchs', 'strSeason', 'strHomeTeam', 'last5MatchsLoss',
         'strAwayTeam', 'last5MatchsWins', 'intRound', 'last5MatchsConcededGoals', 'last5MatchsScoredGoals',
         'intHomeScore', 'strSeason', 'score5LastMatchs', 'intAwayScore', 'goalAverageLast5Matchs'])]]

###Transforme les données après transformation et modélisation des données
def cleanPostTransformationEvent(df):
    return df[df.columns[df.columns.isin(
        ['idTeam', 'nameTeam', 'isHome', 'isWinning', 'opponentLast5MatchsScoredGoals', 'opponentNameTeam',
         'opponentLast5MatchsWins', 'opponentLast5MatchsLoss', 'opponentLast5MatchsConcededGoals',
         'opponentScore5LastMatchs', 'opponentGoalAverageLast5Matchs', 'scoredGoals', 'last5MatchsLoss',
         'concededGoals', 'last5MatchsWins', 'score5LastMatchs', 'goalAverageLast5Matchs', 'last5MatchsConcededGoals',
         'last5MatchsScoredGoals'])]]
