from FootballClasses import *
from datetime import datetime
from UtilsAndGlobals import *
import re, json
class DatosTemporada:

    def __init__(self, division, temporada, globalTeamIds):
        self.division = division
        self.temporada = temporada
        self.numJornadas = 2*(len(globalTeamIds)-1)

        temporadaAñoStart = int(temporada.split("-")[0])
        self.puntosPorVictoria = 3 if temporadaAñoStart > 1994 else 2

        self.clasificacion = dict()
        self.golesafavor = dict()
        self.golesencontra = dict()
        self.jornadas = dict()
        for equipoId in globalTeamIds:
            self.clasificacion[equipoId] = 0
            self.golesafavor[equipoId] = 0
            self.golesencontra[equipoId] = 0


    def addMatch(self, jornada, fecha, localGlobalId, visitanteGlobalId, golesLocal, golesVisitante):
        global CURRENT_MATCH_ID
        matchDate = datetime.strptime(fecha, '%d/%m/%Y')
        localName = IDs_TO_TEAM[localGlobalId].nombre
        visitanteName = IDs_TO_TEAM[visitanteGlobalId].nombre
        print("jornada-{}, fecha-{}, local-{}-{}, visitante-{}-{}, golesLocal-{}, golesVisitante-{}".format(jornada, fecha, localName, localGlobalId, visitanteName, visitanteGlobalId, golesLocal, golesVisitante))
        localValue = GET_MARKET_VALUE(localName, matchDate)
        visitanteValue = GET_MARKET_VALUE(visitanteName, matchDate)

        # print(localName, matchDate.strftime("%d/%m/%Y"), localValue)
        # print(visitanteName, matchDate.strftime("%d/%m/%Y"), visitanteValue)

        if jornada not in self.jornadas:
            self.jornadas[jornada] = dict()
        self.jornadas[jornada][CURRENT_MATCH_ID] = Partido(CURRENT_MATCH_ID, self.division, self.temporada, jornada, fecha,
                                                            localGlobalId, localValue, self.clasificacion[localGlobalId],
                                                            self.golesafavor[localGlobalId], self.golesencontra[localGlobalId],
                                                            visitanteGlobalId, visitanteValue,self.clasificacion[visitanteGlobalId],
                                                            self.golesafavor[visitanteGlobalId], self.golesencontra[visitanteGlobalId],
                                                            golesLocal, golesVisitante)

        puntosLocal = self.puntosPorVictoria if golesLocal>golesVisitante else (1 if golesLocal==golesVisitante else 0)
        puntosVisitante = self.puntosPorVictoria if golesVisitante>golesLocal else (1 if golesLocal==golesVisitante else 0)
        self.clasificacion[localGlobalId] += puntosLocal
        self.clasificacion[visitanteGlobalId] += puntosVisitante
        self.golesafavor[localGlobalId] += golesLocal
        self.golesafavor[visitanteGlobalId] += golesVisitante
        self.golesencontra[localGlobalId] += golesVisitante
        self.golesencontra[visitanteGlobalId] += golesLocal
        self.orderClassification()
        CURRENT_MATCH_ID = CURRENT_MATCH_ID + 1
        
    # Obtengo una lista con los partidos de futbol de una temporada
    def fillSeason(self, parsedSeasonData, seasonTeamsIdToGlobalId):
        # matches = re.findall(r'SP\[\d{0,100}\]\[\d{0,100}\]=\".*?\";', str_partidos)
        matches = re.findall(r'SP\[\d{0,100}\].push\(.*\);', parsedSeasonData)
        for matchData in matches:
            jornada = re.findall(r'SP\[.*?]', matchData)[0].replace('SP[', '').replace(']', '')
            jsonInfo = json.loads(re.findall(r'\{.*\}', matchData)[0])
            fecha = jsonInfo.get("d")
            localGlobalId = seasonTeamsIdToGlobalId[int(jsonInfo.get("a1"))]
            visitanteGlobalId = seasonTeamsIdToGlobalId[int(jsonInfo.get("a2"))]
            golesLocal = int(jsonInfo.get("g1"))
            golesVisitante = int(jsonInfo.get("g2"))
            self.addMatch(jornada, fecha, localGlobalId, visitanteGlobalId, golesLocal, golesVisitante)



    def orderClassification(self):
        self.clasificacion = {k: v for k, v in sorted(self.clasificacion.items(), reverse=True, key=lambda item: item[1])}


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
        maxPuntos = max(self.clasificacion.items(), key=lambda x: x[1])[1]
        equiposGanadores = [equipoId for equipoId, puntos in self.clasificacion.items() if puntos == maxPuntos]

        if len(equiposGanadores)>1:
            nombreGanador = TIED_SEASON_WINNERS[self.division][self.temporada]
            teamID = TEAM_NAMES_TO_ID[nombreGanador]
            print("EMPATE: GANADOR->",IDs_TO_TEAM[teamID])
        else:
            print(IDs_TO_TEAM[equiposGanadores[0]])

