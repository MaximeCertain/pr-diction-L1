<script>
    import Select from 'svelte-select';
    let apiPort =  '9001'
    let message = "";
    let teamsL1 = []
    let undefined = "";
    getTeamsLs()
    let selectedValueA = 134709;
    let selectedValueB = 133822;
    let resultPrediction = ""
    let teamAInfos={'logo':'','jersey':''}
    let teamBInfos={'logo':'','jersey':''}


    async function trainMachine() {
        let response = await fetch(`http://127.0.0.1:${apiPort}/training`);
        let text = await response.json();
        message = `Le modèle a été entrainé, le taux de précision est de ${text.accuracyScore} %`
        return text;
    }

    async function getTeamsLs() {
        let response = await fetch(`https://www.thesportsdb.com/api/v1/json/1/search_all_teams.php?l=French%20Ligue%201`);
        let teams = await response.json();
        teamsL1 = teams["teams"]
    }

    async function predictOpposition() {

        let response = await fetch(`http://127.0.0.1:${apiPort}/predict?idTeamA=${selectedValueA}&idTeamB=${selectedValueB}`);
        let result = await response.json();
        resultPrediction =` Equipe A : ${result['A']} %  Equipe B : ${result['B']} %`
        let teamA  = teamsL1.filter(team => team.idTeam === selectedValueA);
        let teamB  = teamsL1.filter(team => team.idTeam === selectedValueB);

        if(teamA[0] !== "undefined"){
            teamAInfos.logo = teamA[0].strTeamBadge
            teamAInfos.jersey = (teamA[0].strTeamJersey)
        }
          if(teamB[0] !== "undefined"){
            teamBInfos.logo = teamB[0].strTeamBadge
            teamBInfos.jersey = (teamB[0].strTeamJersey)
        }
    }

    function handleChange(event) {
        if (event.target.name === "selectedValueA") {
            selectedValueA = event.target.value
        } else {
            selectedValueB = event.target.value
        }
    }
</script>

<main>
    <h1>Ligue 1 Uber-Eat</h1>
    <p>Prédiction de matchs</p>
    <button class="btnTrain" on:click={trainMachine}>Entrainer mon modèle</button>
    <p>{message}</p>
    <hr>
    <h2>Prédiction sur une opposition</h2>
    <label>Choisir l'équipe à domicile
        <select value={selectedValueA} name="selectedValueA" on:change={handleChange}>
            {#if teamsL1 != null}
                {#each teamsL1 as team}
                    <option value={team.idTeam}>
                        {team.strTeam}
                    </option>
                {/each}
            {/if}
        </select>
    </label>
    <label>Choisir l'équipe à l'extérieur
        <select value={selectedValueB} name="selectedValueB" on:change={handleChange}>
            {#if teamsL1 != null}
                {#each teamsL1 as team}
                    <option value={team.idTeam}>
                        {team.strTeam}
                    </option>
                {/each}
            {/if}
        </select>
    </label>
    <button class="btnTrain" on:click={predictOpposition}>Prédire</button>
    <h2>{resultPrediction}</h2>
    <div class="containerResult" >
        <div class="Aresult">
            {#if teamAInfos.logo != null}
            <img src="{teamAInfos.logo}">
            <img src="{teamAInfos.jersey}">
        {/if}
        </div>
        <div class="Bresult">
            {#if teamBInfos.logo != null}
            <img src="{teamBInfos.logo}">
            <img src="{teamBInfos.jersey}">
        {/if}
        </div>
    </div>

</main>

<style>
    .containerResult{
        display: flex;
    }
     .Aresult{
        width: 50%;
         float: left;
    }
     .Aresult > img, .Bresult > img{
         width: 100px;
     }
      .Bresult{
         width: 50%;
         float: right;
    }
    main {
        text-align: center;
        padding: 1em;
        max-width: 240px;
        margin: 0 auto;
    }

    h1 {
        color: #ff3e00;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
    }

    .btnTrain {
        border-radius: 15px;
        background-color: #ff3e00;
        color: #ffffff
    }

    @media (min-width: 640px) {
        main {
            max-width: none;
        }
    }
</style>