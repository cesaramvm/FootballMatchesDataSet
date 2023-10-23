import UtilsAndGlobals as ut
import csv


teamsSeasonIdToGlobalId = dict()

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
    teamsNames = list({(d['localName'], d["localId"]) for d in filteredRows})
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
    # idPartido;division;temporada;jornada;matchDate;
    # localName;localId;localMarketValue;puntosLocal;golesafavorlocal;golesencontralocal;
    # visitanteName;visitanteId;visitanteMarketValue;puntosVisitante;golesafavorvisitante;golesencontravisitante;
    # golesLocal;golesVisitante;golDiff
    for match in filteredRows:
        jornada = int(match["jornada"])
        matchDate = match["matchDate"]
        localGlobalId = teamsSeasonIdToGlobalId[int(match["localId"])]
        localName = match["localName"]
        visitanteGlobalId = teamsSeasonIdToGlobalId[int(match["visitanteId"])]
        visitanteName = match["visitanteName"]
        golesLocal = int(match["golesLocal"])
        golesVisitante = int(match["golesVisitante"])
        golDiff = int(match["golDiff"])
        matchesArray.append([jornada, matchDate, localGlobalId, localName, visitanteGlobalId, visitanteName, golesLocal, golesVisitante,golDiff])
    return matchesArray

