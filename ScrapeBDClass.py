import sys
import Const
from bs4 import BeautifulSoup
import requests, re, json
from FutbolClasses import Partido

class ScrapeBDFutbol:

    def __init__(self):
        self.temporada = dict()
        self.partidos = dict()
        self.currentTeamsId = dict()
        self.idToEquipoDict = dict()
        self.equipoToIdDict = dict()
        self.equipoCount = 0
        self.contador = 0

    def startScrape(self):
        for season in Const.TEMPORADAS:
            print("****  PROCESANDO TEMPORADA %s ****" % season)
            for division in range(1,3):
                self.currentTeamsId = dict()
                resultScrape = self.scrapeLeague(division, season)
                self.temporada[season] = {division:resultScrape}

    def scrapeLeague(self, division, season):
        url = Const.URLS[division]  % season
        req = requests.get(url)
        soupReq = BeautifulSoup(req.text, "html.parser")
        seasonData = str(soupReq.find('div', {'id': 'resultats'}))
        self.findEquipos(seasonData)
        self.findPartidos(seasonData, season, division)

    def saveInfo(self, fileName):
        fichero = open(fileName, 'w')
        fichero.write('idPartido::temporada::division::jornada::EquipoLocal::'
                      'EquipoVisitante::golesLocal::golesVisitante::fecha\n')
        for value in self.partidos.values():
            fichero.write('%s\n' % str(value))

    # Funcion para sustituir el nombre de los equipos y unificarlos
    def replaceEquipos(self, equipo):
        if equipo not in Const.NAMES_CORRECTION:
            print(equipo + " no está en la corrección")
            sys.exit(1)
        else:
            equipo = Const.NAMES_CORRECTION[equipo]
        return equipo

    # Inserto los equipos nuevos en el diccionario
    def findEquipos(self, str_resultados):
        match = re.findall(r'SE\[\d{0,100}\]=\".*?\";', str_resultados)
        for mat in match:
            mat = re.sub(r'SE.*?="', '', mat)
            mat = mat.replace('";', '')
            sp = mat.split('|')
            # Todo guardar en un diccionario temporal
            currentEquipoId = int(sp[0])
            equipo = sp[1]
            newEquipoName = self.replaceEquipos(equipo)
            self.currentTeamsId[currentEquipoId] = newEquipoName

            if not newEquipoName in self.equipoToIdDict:
                self.idToEquipoDict[self.equipoCount] = newEquipoName
                self.equipoToIdDict[newEquipoName] = self.equipoCount
                self.equipoCount = self.equipoCount + 1

    # Obtengo una lista con los partidos de futbol de una temporada
    def findPartidos(self, str_partidos, temporada, division):
        # matches = re.findall(r'SP\[\d{0,100}\]\[\d{0,100}\]=\".*?\";', str_partidos)
        matches = re.findall(r'SP\[\d{0,100}\].push\(.*\);', str_partidos)
        for matchData in matches:
            jornada = re.findall(r'SP\[.*?]', matchData)[0].replace('SP[', '').replace(']', '')
            jsonInfo = json.loads(re.findall(r'\{.*\}', matchData)[0])
            dia = jsonInfo.get("d")
            eq1Id = int(jsonInfo.get("a1"))
            eq2Id = int(jsonInfo.get("a2"))
            score1 = int(jsonInfo.get("g1"))
            score2 = int(jsonInfo.get("g2"))
            self.contador += 1
            local = self.replaceEquipos(self.currentTeamsId[eq1Id])
            visitante = self.replaceEquipos(self.currentTeamsId[eq2Id])
            self.partidos[self.contador] = Partido(self.contador, temporada, division, jornada, local,
                                         visitante, score1, score2, dia)
