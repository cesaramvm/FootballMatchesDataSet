from FutbolClasses import *
from datetime import datetime
from UtilsAndGlobals import *
import requests, re, json
from bs4 import BeautifulSoup
class DatosTemporada:

    def __init__(self, division, temporada, globalTeamIds):
        self.division = division
        self.temporada = temporada
        self.numJornadas = 2*(len(globalTeamIds)-1)

        temporadaAñoStart = int(temporada.split("-")[0])
        self.puntosPorVictoria = 3 if temporadaAñoStart > 1994 else 2

        self.clasificacion = dict()
        self.jornadas = dict()
        for equipoId in globalTeamIds:
            self.clasificacion[equipoId] = 0

    def addMatch(self, jornada, fecha, localId, visitanteId, golesLocal, golesVisitante):
        global CURRENT_MATCH_ID
        matchDate = datetime.strptime(fecha, '%d/%m/%Y')
        firstMarketDate = datetime(2010, 8, 1)

        localNombre = IDs_TO_TEAM[localId].nombre
        visitanteNombre = IDs_TO_TEAM[visitanteId].nombre
        if(matchDate>firstMarketDate):
            localValue = -1
            visitanteValue = -1
            localMarketName = MARKET_NAMES_CORRECTION.get(localNombre)
            visitanteMarketName = MARKET_NAMES_CORRECTION.get(visitanteNombre)

            marketDate = min(FECHAS_VALORES, key=lambda sub: abs(sub - matchDate))
            marketUrl = MARKET_URL % marketDate.strftime("%Y-%m-%d")
            req = requests.get(marketUrl, headers={'User-Agent': 'Custom'})

            print(localNombre, "-", visitanteNombre)
            if (localMarketName):
                localMarketNode = BeautifulSoup(req.text, "html.parser").find('td', {'class': 'hauptlink no-border-links'}, string=localMarketName)
                localValue = localMarketNode.find_next_siblings()[1].find("a").string
            if (visitanteMarketName):
                visitanteMarketNode = BeautifulSoup(req.text, "html.parser").find('td',{'class': 'hauptlink no-border-links'},string=visitanteMarketName)
                visitanteValue = visitanteMarketNode.find_next_siblings()[1].find("a").string


        if jornada not in self.jornadas:
            self.jornadas[jornada] = dict()
        self.jornadas[jornada][CURRENT_MATCH_ID] = Partido(CURRENT_MATCH_ID, self.division, self.temporada, jornada, fecha,
                                                           localId, visitanteId,
                                                           self.clasificacion[localId], self.clasificacion[visitanteId],
                                                           golesLocal, golesVisitante)

        puntosLocal = self.puntosPorVictoria if golesLocal>golesVisitante else (1 if golesLocal==golesVisitante else 0)
        puntosVisitante = self.puntosPorVictoria if golesVisitante>golesLocal else (1 if golesLocal==golesVisitante else 0)
        self.clasificacion[localId] += puntosLocal
        self.clasificacion[visitanteId] += puntosVisitante

        CURRENT_MATCH_ID = CURRENT_MATCH_ID + 1

    def printSeasonResults(self):
        clasiOrdenada = {k: v for k, v in sorted(self.clasificacion.items(), reverse=True, key=lambda item: item[1])}
        iteration = iter(clasiOrdenada)
        for i in range(1,4):
            equipoId = next(iteration)
            puntosEquipo = str(IDs_TO_TEAM[equipoId]) + " " + str(self.clasificacion[equipoId])
            print(puntosEquipo)

        clasiOrdenada = {IDs_TO_TEAM[k]: v for k, v in sorted(self.clasificacion.items(), reverse=True, key=lambda item: item[1])}
        print(clasiOrdenada)


    def printSeasonWinner(self):
        clasiOrdenada = {k: v for k, v in sorted(self.clasificacion.items(), reverse=True, key=lambda item: item[1])}
        iteration = iter(clasiOrdenada)
        for i in range(1,2):
            equipoId = next(iteration)
            puntosEquipo = str(IDs_TO_TEAM[equipoId]) + " " + str(self.clasificacion[equipoId])
            print(puntosEquipo)
