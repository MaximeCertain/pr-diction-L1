<h1>Prédiction de matchs de ligue 1</h1>
<hr>


<h3>Accèder à l'API</h3>

<P>docker build -t betml . <br>
docker run -p 0.0.0.0:9001:9032 --net=host betml
<br>
Vous pouvez utiliser l'API à l'adresse http://0.0.0.0:9001/ (exemple d'utilisation dans le notebook main.ipynb)
<h5>route /training</h5>
<p>Cette route permet d'entrainer la machine à partir des données fournies par l'API. Retourne le taux de précision </p>
<h5>route /predict?idTeamA=x&idTeamB=y</h5>
<p>Cette route va prédire le probabilité de victoire de chacune des équipes. Elle fournit en retour un pourcentage pour chacune des deux équipes </p>


<h3>Accèder à l'application web</h3>


cd front
docker build -t frontbet .
docker run -p 0.0.0.0:9002:9033 --net=host frontbet

<p>Se rendre sur l'adresse fournie par le docker run</p>
<p>Vous pouvez entraîner votre machine ou bien faire une prédiction entre deux équipes et apprécier le résultat</p>
