from bs4 import BeautifulSoup
import UtilsAndGlobals as ut
import requests, re, json
from datetime import datetime

class WebScraper:
    def __init__(self, division, temporada):
        self.data = self.filterData(division, temporada)
        self.teamsSeasonIdToGlobalIdDict = self.getTeamsSeasonIdToGlobalIdDict()
        self.matchesArray = self.getMatchesArray()

    def filterData(self, division, temporada):
        url = ut.URLS[division] % temporada
        req = requests.get(url)
        return str(BeautifulSoup(req.text, "html.parser").find('div', {'id': 'resultats'}))

    def getTeamsSeasonIdToGlobalIdDict(self):
        seasonIdToGlobalId = {}
        match = re.findall(r'SE\[\d{0,100}\]=\".*?\";', self.data)
        for mat in match:
            mat = re.sub(r'SE.*?="', '', mat)
            mat = mat.replace('";', '')
            sp = mat.split('|')
            seasonTeamId = int(sp[0])
            teamName = ut.CHECK_EQUIPO_NAME(sp[1])
            globalTeamId = ut.CHECK_EQUIPO_ID(teamName)
            seasonIdToGlobalId[seasonTeamId] = globalTeamId
        return seasonIdToGlobalId


    def getMatchesArray(self):
        # matches = re.findall(r'SP\[\d{0,100}\]\[\d{0,100}\]=\".*?\";', str_partidos)
        matches = re.findall(r'SP\[\d{0,100}\].push\(.*\);', self.data)
        matchesArray = []
        for matchData in matches:
            jornada = re.findall(r'SP\[.*?]', matchData)[0].replace('SP[', '').replace(']', '')
            jsonInfo = json.loads(re.findall(r'\{.*\}', matchData)[0])
            matchDate = datetime.strptime(jsonInfo.get("d"), '%d/%m/%Y').strftime('%Y-%m-%d')
            localGlobalId = self.teamsSeasonIdToGlobalIdDict[int(jsonInfo.get("a1"))]
            localName = ut.IDs_TO_TEAM[localGlobalId]
            visitanteGlobalId = self.teamsSeasonIdToGlobalIdDict[int(jsonInfo.get("a2"))]
            visitanteName = ut.IDs_TO_TEAM[visitanteGlobalId]
            golesLocal = int(jsonInfo.get("g1"))
            golesVisitante = int(jsonInfo.get("g2"))
            golDiff = golesLocal-golesVisitante
            matchesArray.append([jornada, matchDate, localGlobalId, localName, visitanteGlobalId, visitanteName, golesLocal, golesVisitante,golDiff])
        return matchesArray



