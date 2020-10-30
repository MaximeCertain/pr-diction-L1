from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from thesportsdb.Modelization import *
from thesportsdb.Cleaner import *
import pandas as pd
from thesportsdb.StaticInfos import StaticInfos
from sklearn.model_selection import train_test_split
import pickle

from thesportsdb.TheSportsDbRepository import getNextRoundId, getEventRoundForLigue

##Entraine la machine à partir des 100 derniers matchs de L1
def trainMachine():
    nextRoundId = getNextRoundId() - 1
    matchsForRound = (getEventRoundForLigue(StaticInfos.ligue1Id, nextRoundId))
    df = pd.DataFrame(matchsForRound)
    df = cleanEvents(df)
    dfTotal = pd.DataFrame()
    load5LastMatchs(nextRoundId)
    for i in range(0, len(df)):
        print("===============================================")
        print(i)
        match = df.iloc[i]
        awayDataframe = getDataframe(int(match['idAwayTeam']))
        homeDataframe = getDataframe(int(match['idHomeTeam']))
        if dfTotal.empty:
            dfTotal = pd.concat([awayDataframe, homeDataframe])
        else:
            dfMatch = pd.concat([awayDataframe, homeDataframe])
            dfTotal = pd.concat([dfTotal, dfMatch])
    return trainMachineWithRandomForestClassifier(dfTotal)


def trainMachineWithRandomForest(dataFrame):
    X = dataFrame[['isWinning', 'isHome', 'last5MatchsWins', 'last5MatchsLoss', 'opponentGoalAverageLast5Matchs',
                   'last5MatchsConcededGoals', 'opponentLast5MatchsLoss', 'opponentLast5MatchsWins',
                   'opponentLast5MatchsConcededGoals', 'opponentLast5MatchsScoredGoals',
                   'last5MatchsScoredGoals', 'score5LastMatchs', 'goalAverageLast5Matchs', 'opponentScore5LastMatchs']]
    y = dataFrame['isWinning'].copy()
    del X['isWinning']
    cls = RandomForestRegressor(max_depth=16, n_estimators=150, random_state=0).fit(X, y)
    score = cls.score(X, y)
    filename = StaticInfos.pickleFileName
    pickle.dump(cls, open(filename, 'wb'))
    return score


def trainMachineWithLogisticRegression(dataFrame):
    X = dataFrame[['isWinning', 'isHome', 'last5MatchsWins', 'last5MatchsLoss', 'opponentGoalAverageLast5Matchs',
                   'last5MatchsConcededGoals', 'opponentLast5MatchsLoss', 'opponentLast5MatchsWins',
                   'opponentLast5MatchsConcededGoals', 'opponentLast5MatchsScoredGoals',
                   'last5MatchsScoredGoals', 'score5LastMatchs', 'goalAverageLast5Matchs', 'opponentScore5LastMatchs']]
    y = dataFrame['isWinning']
    x_train, x_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
    cls = LogisticRegression(max_iter=300).fit(x_train, y_train)
    score = cls.score(x_val, y_val)
    filename = StaticInfos.pickleFileName
    pickle.dump(cls, open(filename, 'wb'))
    return score


def trainMachineWithRandomForestClassifier(dataFrame):
    X = dataFrame[['isWinning', 'isHome', 'last5MatchsWins', 'last5MatchsLoss', 'opponentGoalAverageLast5Matchs',
                   'last5MatchsConcededGoals', 'opponentLast5MatchsLoss', 'opponentLast5MatchsWins',
                   'opponentLast5MatchsConcededGoals', 'opponentLast5MatchsScoredGoals',
                   'last5MatchsScoredGoals', 'score5LastMatchs', 'goalAverageLast5Matchs', 'opponentScore5LastMatchs']]
    y = dataFrame['isWinning']
    del X['isWinning']
    x_train, x_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
    cls = RandomForestClassifier(n_estimators=200, max_depth=2).fit(x_train, y_train)
    score = cls.score(x_val, y_val)
    filename = StaticInfos.pickleFileName
    pickle.dump(cls, open(filename, 'wb'))
    return score


def trainMachineWithGradientBoostingClassifier(dataFrame):
    X = dataFrame[['isWinning', 'isHome', 'last5MatchsWins', 'last5MatchsLoss', 'opponentGoalAverageLast5Matchs',
                   'last5MatchsConcededGoals', 'opponentLast5MatchsLoss', 'opponentLast5MatchsWins',
                   'opponentLast5MatchsConcededGoals', 'opponentLast5MatchsScoredGoals',
                   'last5MatchsScoredGoals', 'score5LastMatchs', 'goalAverageLast5Matchs', 'opponentScore5LastMatchs']]
    y = dataFrame['isWinning']
    x_train, x_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
    cls = GradientBoostingClassifier(random_state=0).fit(x_train, y_train)
    score = cls.score(x_val, y_val)
    filename = StaticInfos.pickleFileName
    pickle.dump(cls, open(filename, 'wb'))
    return score
