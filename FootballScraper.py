from UtilsAndGlobals import *
from bs4 import BeautifulSoup
import requests, re, json
from DatosTemporada import DatosTemporada


def startScrape():
    for division in range(1, 3):
        print("****  PROCESANDO DIVISIÓN %s ****" % division)
        for season in TEMPORADAS:
            print("****  PROCESANDO TEMPORADA %s ****" % season)
            scrapeLeague(division, season)


def scrapeLeague(division, temporada):
    url = URLS[division] % temporada
    req = requests.get(url)
    soupReq = BeautifulSoup(req.text, "html.parser")
    parsedSeasonData = str(soupReq.find('div', {'id': 'resultats'}))
    seasonIdToGlobalId = findEquipos(parsedSeasonData)
    datosTemporada = DatosTemporada(division, temporada, seasonIdToGlobalId)
    fillSeason(datosTemporada, parsedSeasonData)
    datosTemporada.printSeasonResults()
    ADD_SEASON_INFO(division, temporada, datosTemporada)


def saveInfo(fileName):
    SAVE_ALL_SEASONS(fileName)


def findEquipos(str_resultados):
    seasonIdToGlobalId = dict()
    match = re.findall(r'SE\[\d{0,100}\]=\".*?\";', str_resultados)
    for mat in match:
        mat = re.sub(r'SE.*?="', '', mat)
        mat = mat.replace('";', '')
        sp = mat.split('|')
        currentEquipoId = int(sp[0])
        equipoName = CHECK_EQUIPO_NAME(sp[1])

        if not equipoName in ALL_TEAMS_TO_ID:
            global CURRENT_TEAM_ID
            ALL_IDS_TO_TEAM[CURRENT_TEAM_ID] = equipoName
            ALL_TEAMS_TO_ID[equipoName] = CURRENT_TEAM_ID
            globalEquipoId = CURRENT_TEAM_ID
            CURRENT_TEAM_ID = CURRENT_TEAM_ID + 1
        else:
            globalEquipoId = ALL_TEAMS_TO_ID[equipoName]

        #TODO Esto de aqui está tremendamente mal. coge la id por la que vayamos del equipo que sea y arreando.
        seasonIdToGlobalId[currentEquipoId] = globalEquipoId


    return seasonIdToGlobalId


# Obtengo una lista con los partidos de futbol de una temporada
def fillSeason(datosTemporada, str_partidos):
    # matches = re.findall(r'SP\[\d{0,100}\]\[\d{0,100}\]=\".*?\";', str_partidos)
    matches = re.findall(r'SP\[\d{0,100}\].push\(.*\);', str_partidos)
    for matchData in matches:
        jornada = re.findall(r'SP\[.*?]', matchData)[0].replace('SP[', '').replace(']', '')
        jsonInfo = json.loads(re.findall(r'\{.*\}', matchData)[0])
        fecha = jsonInfo.get("d")
        localId = int(jsonInfo.get("a1"))
        visitanteId = int(jsonInfo.get("a2"))
        golesLocal = int(jsonInfo.get("g1"))
        golesVisitante = int(jsonInfo.get("g2"))
        datosTemporada.addMatch(jornada, fecha, localId, visitanteId, golesLocal, golesVisitante)

    return datosTemporada
