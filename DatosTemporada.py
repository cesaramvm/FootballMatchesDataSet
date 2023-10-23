import FootballClasses as fc
import UtilsAndGlobals as ut
from FileScraper import FileScraper 
from WebScraper import WebScraper
import os
from colorama import Fore, Back, Style

class DatosTemporada:

    def __init__(self, division, temporada, loadFromFile):
        self.seasonLoader = FileScraper(division, temporada) if loadFromFile else WebScraper(division, temporada)
        self.division = division
        self.temporada = temporada

        temporadaAñoStart = int(temporada.split("-")[0])
        self.puntosPorVictoria = 3 if temporadaAñoStart > 1994 else 2

        self.clasificacion = dict()
        self.golesafavor = dict()
        self.golesencontra = dict()
        self.jornadas = dict()

        self.loadEquipos()
        self.loadMatches()
    

    def loadEquipos(self):
        if len(self.seasonLoader.teamsSeasonIdToGlobalIdDict) ==0:
            raise Exception("NO HAY EQUIPOS QUE CARGAR")
        self.numJornadas = 2*(len(self.seasonLoader.teamsSeasonIdToGlobalIdDict)-1)
        for equipoId in self.seasonLoader.teamsSeasonIdToGlobalIdDict.values():
            self.clasificacion[equipoId] = 0
            self.golesafavor[equipoId] = 0
            self.golesencontra[equipoId] = 0
    
    def loadMatches(self):
        if len(self.seasonLoader.matchesArray) ==0:
            raise Exception("NO HAY PARTIDOS QUE CARGAR")
        for match in self.seasonLoader.matchesArray:
            jornada = match[0]
            matchDate = match[1]
            localGlobalId = match[2]
            localName = match[3]
            visitanteGlobalId = match[4]
            visitanteName =match[5]
            golesLocal = match[6]
            golesVisitante = match[7]
            golDiff = match[8]
            self.addMatch(self.division, jornada, matchDate, localGlobalId, localName, visitanteGlobalId, visitanteName, golesLocal, golesVisitante,golDiff)

    def addMatch(self, division, jornada, matchDate, localGlobalId, localName, visitanteGlobalId, visitanteName, golesLocal, golesVisitante,golDiff):
        localName = ut.IDs_TO_TEAM[localGlobalId].nombre
        visitanteName = ut.IDs_TO_TEAM[visitanteGlobalId].nombre
        #print("jornada-{}, fecha-{}, local-{}-{}, visitante-{}-{}, golesLocal-{}, golesVisitante-{}".format(jornada, matchDate, localName, localGlobalId, visitanteName, visitanteGlobalId, golesLocal, golesVisitante))
        teamsValues = ut.getTeamsMarketValue(division, matchDate, localName, visitanteName)   
        localMarketValue = teamsValues[0]
        visitanteMarketValue = teamsValues[1]

        if jornada not in self.jornadas:
            self.jornadas[jornada] = dict()
        self.jornadas[jornada][ut.CURRENT_MATCH_ID] = fc.Partido(ut.CURRENT_MATCH_ID, self.division, self.temporada, jornada, matchDate,
                                                            localName, localGlobalId, localMarketValue, self.clasificacion[localGlobalId],
                                                            self.golesafavor[localGlobalId], self.golesencontra[localGlobalId],
                                                            visitanteName, visitanteGlobalId, visitanteMarketValue,self.clasificacion[visitanteGlobalId],
                                                            self.golesafavor[visitanteGlobalId], self.golesencontra[visitanteGlobalId],
                                                            golesLocal, golesVisitante, golDiff)
        self.updateClassification(golesLocal, golesVisitante, localGlobalId, visitanteGlobalId)
        ut.CURRENT_MATCH_ID += 1
        

    def updateClassification(self, golesLocal, golesVisitante, localGlobalId, visitanteGlobalId):
        puntosLocal = self.puntosPorVictoria if golesLocal>golesVisitante else (1 if golesLocal==golesVisitante else 0)
        puntosVisitante = self.puntosPorVictoria if golesVisitante>golesLocal else (1 if golesLocal==golesVisitante else 0)
        self.clasificacion[localGlobalId] += puntosLocal
        self.clasificacion[visitanteGlobalId] += puntosVisitante
        self.golesafavor[localGlobalId] += golesLocal
        self.golesafavor[visitanteGlobalId] += golesVisitante
        self.golesencontra[localGlobalId] += golesVisitante
        self.golesencontra[visitanteGlobalId] += golesLocal
        self.clasificacion = {k: v for k, v in sorted(self.clasificacion.items(), reverse=True, key=lambda item: item[1])}


    def printSeasonResults(self):
        clasiOrdenada = {k: v for k, v in sorted(self.clasificacion.items(), reverse=True, key=lambda item: item[1])}
        iteration = iter(clasiOrdenada)
        for i in range(1,4):
            equipoId = next(iteration)
            puntosEquipo = str(ut.IDs_TO_TEAM[equipoId]) + " " + str(self.clasificacion[equipoId])
            print(puntosEquipo)

        clasiOrdenada = {ut.IDs_TO_TEAM[k]: v for k, v in sorted(self.clasificacion.items(), reverse=True, key=lambda item: item[1])}
        print(clasiOrdenada)


    def printSeasonWinner(self):
        maxPuntos = max(self.clasificacion.items(), key=lambda x: x[1])[1]
        equiposGanadores = [equipoId for equipoId, puntos in self.clasificacion.items() if puntos == maxPuntos]

        if len(equiposGanadores)>1:
            nombreGanador = ut.TIED_SEASON_WINNERS[self.division][self.temporada]
            teamID = ut.TEAM_NAMES_TO_ID[nombreGanador]
            print("EMPATE: GANADOR->",ut.IDs_TO_TEAM[teamID])
        else:
            print(ut.IDs_TO_TEAM[equiposGanadores[0]])

