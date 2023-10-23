import UtilsAndGlobals as ut
import csv

teamsSeasonIdToGlobalId = dict()
    
    # with open(ut.SAVE_FILE, 'r') as file:
    #     next(file)
    #     filtered_rows = []
    #     for line in file:
    #         parts = line.strip().split(';')


def filterData(division, temporada):
    filteredRows = []
    # Open the CSV file and read it row by row
    with open(ut.SAVE_SEASONS_PATH, 'r', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            rowDivision = int(row['division'])
            rowSeason = row['temporada']
            if rowDivision == division and rowSeason == temporada:
                filteredRows.append(row)
    return filteredRows
    

            
def getKeysDictAndMatches(division, temporada):
    #TODO filtrar la división y temporada del csv y pasarselo como argumento a las funcinoes
    filteredRows = filterData(division,temporada)
    return [getTeamsSeasonIdToGlobalIdDict(filteredRows), getMatchesArray(filteredRows)]

def getTeamsSeasonIdToGlobalIdDict(filteredRows):
    global teamsSeasonIdToGlobalId
    seasonIdToGlobalId = dict()
    teamsNames = list({(d['LocalName'], d["EquipoLocalId"]) for d in filteredRows})
    for team in teamsNames:
        seasonTeamId = int(team[1])
        teamName = ut.CHECK_EQUIPO_NAME(team[0])
        globalTeamId = ut.CHECK_EQUIPO_ID(teamName)
        seasonIdToGlobalId[seasonTeamId] = globalTeamId
    teamsSeasonIdToGlobalId = seasonIdToGlobalId
    return seasonIdToGlobalId


def getMatchesArray(filteredRows):
    global teamsSeasonIdToGlobalId
    matchesArray = []
    for match in filteredRows:
        jornada = int(match["jornada"])
        matchDate = match["matchDate"]
        localGlobalId = teamsSeasonIdToGlobalId[int(match["EquipoLocalId"])]
        localName = match["LocalName"]
        visitanteGlobalId = teamsSeasonIdToGlobalId[int(match["EquipoVisitanteId"])]
        visitanteName = match["VisitanteName"]
        golesLocal = int(match["golesLocal"])
        golesVisitante = int(match["golesVisitante"])
        golDiff = int(match["golDiff"])
        matchesArray.append([jornada, matchDate, localGlobalId, localName, visitanteGlobalId, visitanteName, golesLocal, golesVisitante,golDiff])
    return matchesArray

