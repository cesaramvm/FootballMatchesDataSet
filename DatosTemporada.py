from FutbolClasses import *
from UtilsAndGlobals import *
class DatosTemporada:

    def __init__(self, division, temporada, seasonIdToGlobalId):
        self.division = division
        self.temporada = temporada
        self.seasonIdToGlobalId = seasonIdToGlobalId
        self.numJornadas = 2*(len(self.seasonIdToGlobalId)-1)

        temporadaAñoStart = int(temporada.split("-")[0])
        self.puntosPorVictoria = 3 if temporadaAñoStart > 1994 else 2

        self.clasificacion = dict()
        self.jornadas = dict()
        for equipoId in seasonIdToGlobalId.values():
            self.clasificacion[equipoId] = 0

    def addMatch(self, jornada, fecha, idLocal, idVisitante, golesLocal, golesVisitante):
        global CURRENT_MATCH_ID
        local = ALL_IDS_TO_TEAM[self.seasonIdToGlobalId[idLocal]]
        visitante = ALL_IDS_TO_TEAM[self.seasonIdToGlobalId[idVisitante]]

        if jornada not in self.jornadas:
            self.jornadas[jornada] = dict()
        partidonuevo = Partido(CURRENT_MATCH_ID, self.division, self.temporada, jornada, fecha,
                               local, visitante, golesLocal, golesVisitante, self.clasificacion[idLocal], self.clasificacion[idVisitante])
        self.jornadas[jornada][CURRENT_MATCH_ID] = partidonuevo

        puntosLocal = self.puntosPorVictoria if golesLocal>golesVisitante else (1 if golesLocal==golesVisitante else 0)
        puntosVisitante = self.puntosPorVictoria if golesVisitante>golesLocal else (1 if golesLocal==golesVisitante else 0)
        self.clasificacion[idLocal] += puntosLocal
        self.clasificacion[idVisitante] += puntosVisitante

        CURRENT_MATCH_ID = CURRENT_MATCH_ID + 1

    def printSeasonResults(self):
        clasiOrdenada = {k: v for k, v in sorted(self.clasificacion.items(), reverse=True, key=lambda item: item[1])}
        iteration = iter(clasiOrdenada)
        for i in range(1,4):
            equipoId = next(iteration)
            puntosEquipo = str(ALL_IDS_TO_TEAM[equipoId]) + " " + str(self.clasificacion[equipoId])
            print(puntosEquipo)


        clasiOrdenada = {ALL_IDS_TO_TEAM[k]: v for k, v in sorted(self.clasificacion.items(), reverse=True, key=lambda item: item[1])}
        print(clasiOrdenada)
