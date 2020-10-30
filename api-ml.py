from flask import Flask, request, jsonify
from flask_cors import CORS

from thesportsdb.Predictor import getPredictionsResult
from thesportsdb.Trainer import trainMachine

app = Flask(__name__)
CORS(app)

###route accueil
@app.route("/")
def home():
    return "Veuillez choisir une route, : /training ou /predict?idTeamA=x&idTamB=y"

###Entraine la machine avec les dernières journées de L1
@app.route("/training")
def training():
    accuracyScore = trainMachine()
    return jsonify({'accuracyScore': (round(accuracyScore, 2) * 100) })

###Prédit la probabilité d'équipe
@app.route("/predict")
def predict():
    idTeamA = request.args.get('idTeamA')
    idTeamB = request.args.get('idTeamB')
    results = getPredictionsResult(idTeamA, idTeamB)

    print(results)
    return jsonify({"A": results[idTeamA], "B": results[idTeamB]})


if __name__ == "__main__":
    app.run(port=9001)