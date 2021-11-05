from FutbolClasses import *
from UtilsAndGlobals import *
class DatosTemporada:

    def __init__(self, division, temporada, seasonIdToTeam):
        self.division = division
        self.temporada = temporada
        self.seasonIdToTeam = seasonIdToTeam

        self.clasificacion = dict()
        self.jornadas = dict()
        for equipoId in seasonIdToTeam.keys():
            self.clasificacion[equipoId] = 0

    def addMatch(self, jornada, fecha, idLocal, idVisitante, golesLocal, golesVisitante):
        global CURRENT_MATCH_ID

        if jornada not in self.jornadas:
            self.jornadas[jornada] = dict()
        partidonuevo = Partido(CURRENT_MATCH_ID, self.division, self.temporada, jornada, fecha,
                               idLocal, idVisitante, golesLocal, golesVisitante, self.clasificacion[idLocal], self.clasificacion[idVisitante])
        self.jornadas[jornada][CURRENT_MATCH_ID] = partidonuevo

        self.updateClasification(idLocal,idVisitante, golesLocal, golesVisitante)

        CURRENT_MATCH_ID = CURRENT_MATCH_ID + 1
        pass

    def updateClasification(self, idLocal, idVisitante, golesLocal, golesVisitante):
        puntosLocal = 3 if golesLocal>golesVisitante else (1 if golesLocal==golesVisitante else 0)
        puntosVisitante = 3 if golesVisitante>golesLocal else (1 if golesLocal==golesVisitante else 0)
        self.clasificacion[idLocal] += puntosLocal
        self.clasificacion[idVisitante] += puntosVisitante
