from UtilsAndGlobals import *
from bs4 import BeautifulSoup
import requests, re, json
from DatosTemporada import DatosTemporada

def startScrape(temporadas):
    for division in range(1, 3):
        print("****  PROCESANDO DIVISIÓN %s ****" % division)
        for temporada in temporadas:
            print("****  PROCESANDO TEMPORADA %s ****" % temporada)
            scrapeLeague(division, temporada)
            # return


def scrapeLeague(division, temporada):
    url = URLS[division] % temporada
    req = requests.get(url)
    parsedSeasonData = str(BeautifulSoup(req.text, "html.parser").find('div', {'id': 'resultats'}))
    seasonTeamsIdToGlobalId = getTeamsIdsToGlobalIdsDict(parsedSeasonData)
    seasonData = DatosTemporada(division, temporada, seasonTeamsIdToGlobalId.values())
    fillSeason(seasonData, parsedSeasonData, seasonTeamsIdToGlobalId)
    # seasonData.printSeasonResults()
    seasonData.printSeasonWinner()
    ADD_SEASON_INFO(division, temporada, seasonData)


def getTeamsIdsToGlobalIdsDict(parsedSeasonData):
    seasonIdToGlobalId = dict()
    match = re.findall(r'SE\[\d{0,100}\]=\".*?\";', parsedSeasonData)
    for mat in match:
        mat = re.sub(r'SE.*?="', '', mat)
        mat = mat.replace('";', '')
        sp = mat.split('|')
        seasonTeamId = int(sp[0])
        teamName = CHECK_EQUIPO_NAME(sp[1])
        globalTeamId = CHECK_EQUIPO_ID(teamName)
        seasonIdToGlobalId[seasonTeamId] = globalTeamId
    return seasonIdToGlobalId


# Obtengo una lista con los partidos de futbol de una temporada
def fillSeason(datosTemporada, parsedSeasonData, seasonTeamsIdToGlobalId):
    # matches = re.findall(r'SP\[\d{0,100}\]\[\d{0,100}\]=\".*?\";', str_partidos)
    matches = re.findall(r'SP\[\d{0,100}\].push\(.*\);', parsedSeasonData)
    for matchData in matches:
        jornada = re.findall(r'SP\[.*?]', matchData)[0].replace('SP[', '').replace(']', '')
        jsonInfo = json.loads(re.findall(r'\{.*\}', matchData)[0])
        fecha = jsonInfo.get("d")
        localId = seasonTeamsIdToGlobalId[int(jsonInfo.get("a1"))]
        visitanteId = seasonTeamsIdToGlobalId[int(jsonInfo.get("a2"))]
        golesLocal = int(jsonInfo.get("g1"))
        golesVisitante = int(jsonInfo.get("g2"))
        datosTemporada.addMatch(jornada, fecha, localId, visitanteId, golesLocal, golesVisitante)

    return datosTemporada


def saveInfo(fileName):
    SAVE_ALL_SEASONS(fileName)

def loadInfo(fileName):
    LOAD_FROM_FILE(fileName)