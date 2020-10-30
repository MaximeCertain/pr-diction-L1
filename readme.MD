<h1>Prédiction de matchs de ligue 1</h1>
<p>Ce projet vise à prédire le pourcentage de chance qu'une équipe batte une autre dans le championnat de Ligue 1</p>
<hr>


<h3>Accèder à l'API</h3>
<ul>
<li>docker build -t betml . <br></li>
<li>docker run -p 0.0.0.0:9001:9032 --net=host betml</li>
<li>Se rendre sur http://0.0.0.0:9001/</li></ul>
<p>Vous pouvez utiliser l'API à l'adresse http://0.0.0.0:9001/ (exemple d'utilisation dans le notebook main.ipynb)</p>
<p>La modélisation et l'entrainement de la machine se fait dans le package thesportdb. Un résumé de ce processus avec analyses des données se trouve dans le fichier main.ipynb </p>
<hr>
<h5>route /training</h5>
<p>Cette route permet d'entrainer la machine à partir des données fournies par l'API. Retourne le taux de précision </p>
<hr>
<h5>route /predict?idTeamA=x&idTeamB=y</h5>
<p>Cette route va prédire le probabilité de victoire de chacune des équipes. Elle fournit en retour un pourcentage pour chacune des deux équipes </p>
<br><hr>
<h3>Accèder à l'application web</h3>

<ul>
<li>cd front</li>
<li>docker build -t frontbet . </li>
<li>docker run -p 0.0.0.0:9002:9033 --net=host frontbet </li>
<li>Se rendre sur l'adresse fournie par le docker run </li>
</ul>
<p>Vous pouvez naviguer sur l'application et entraîner votre machine ou bien faire une prédiction entre deux équipes et apprécier le résultat</p>
