from bs4 import BeautifulSoup
import UtilsAndGlobals as ut
import requests, re, json
from datetime import datetime

teamsSeasonIdToGlobalId = dict()

def getKeysDictAndMatches(division, temporada):
    url = ut.URLS[division] % temporada
    req = requests.get(url)
    parsedSeasonData = str(BeautifulSoup(req.text, "html.parser").find('div', {'id': 'resultats'}))
    return [getTeamsSeasonIdToGlobalIdDict(parsedSeasonData), getMatchesArray(parsedSeasonData)]

def getTeamsSeasonIdToGlobalIdDict(parsedSeasonData):
    global teamsSeasonIdToGlobalId
    seasonIdToGlobalId = dict()
    match = re.findall(r'SE\[\d{0,100}\]=\".*?\";', parsedSeasonData)
    for mat in match:
        mat = re.sub(r'SE.*?="', '', mat)
        mat = mat.replace('";', '')
        sp = mat.split('|')
        seasonTeamId = int(sp[0])
        teamName = ut.CHECK_EQUIPO_NAME(sp[1])
        globalTeamId = ut.CHECK_EQUIPO_ID(teamName)
        seasonIdToGlobalId[seasonTeamId] = globalTeamId
    teamsSeasonIdToGlobalId = seasonIdToGlobalId
    return seasonIdToGlobalId


def getMatchesArray(parsedSeasonData):
    global teamsSeasonIdToGlobalId
    # matches = re.findall(r'SP\[\d{0,100}\]\[\d{0,100}\]=\".*?\";', str_partidos)
    matches = re.findall(r'SP\[\d{0,100}\].push\(.*\);', parsedSeasonData)
    matchesArray = []
    for matchData in matches:
        jornada = re.findall(r'SP\[.*?]', matchData)[0].replace('SP[', '').replace(']', '')
        jsonInfo = json.loads(re.findall(r'\{.*\}', matchData)[0])
        matchDate = datetime.strptime(jsonInfo.get("d"), '%d/%m/%Y').strftime('%Y-%m-%d')
        localGlobalId = teamsSeasonIdToGlobalId[int(jsonInfo.get("a1"))]
        localName = ut.IDs_TO_TEAM[localGlobalId]
        visitanteGlobalId = teamsSeasonIdToGlobalId[int(jsonInfo.get("a2"))]
        visitanteName = ut.IDs_TO_TEAM[visitanteGlobalId]
        golesLocal = int(jsonInfo.get("g1"))
        golesVisitante = int(jsonInfo.get("g2"))
        golDiff = golesLocal-golesVisitante
        matchesArray.append([jornada, matchDate, localGlobalId, localName, visitanteGlobalId, visitanteName, golesLocal, golesVisitante,golDiff])
    return matchesArray



