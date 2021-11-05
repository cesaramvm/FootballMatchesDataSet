from FutbolClasses import *
from UtilsAndGlobals import *
class DatosTemporada:

    def __init__(self, division, temporada, seasonIdToGlobalId):
        self.division = division
        self.temporada = temporada
        self.seasonIdToGlobalId = seasonIdToGlobalId
        temporadaAñoStart = int(temporada.split("-")[0])
        self.puntosPorVictoria = 3 if temporadaAñoStart > 1994 else 2

        self.clasificacion = dict()
        self.jornadas = dict()
        for equipoId in seasonIdToGlobalId.values():
            self.clasificacion[equipoId] = 0

    def addMatch(self, jornada, fecha, idLocal, idVisitante, golesLocal, golesVisitante):
        global CURRENT_MATCH_ID
        idLocal = self.seasonIdToGlobalId[idLocal]
        idVisitante = self.seasonIdToGlobalId[idVisitante]

        if jornada not in self.jornadas:
            self.jornadas[jornada] = dict()
        partidonuevo = Partido(CURRENT_MATCH_ID, self.division, self.temporada, jornada, fecha,
                               idLocal, idVisitante, golesLocal, golesVisitante, self.clasificacion[idLocal], self.clasificacion[idVisitante])
        self.jornadas[jornada][CURRENT_MATCH_ID] = partidonuevo

        puntosLocal = self.puntosPorVictoria if golesLocal>golesVisitante else (1 if golesLocal==golesVisitante else 0)
        puntosVisitante = self.puntosPorVictoria if golesVisitante>golesLocal else (1 if golesLocal==golesVisitante else 0)
        self.clasificacion[idLocal] += puntosLocal
        self.clasificacion[idVisitante] += puntosVisitante

        CURRENT_MATCH_ID = CURRENT_MATCH_ID + 1

