#Autor original Ricardo Moya https://github.com/RicardoMoya/FootballMatchesDataSet
import copy
from dataclasses import dataclass

class Equipo:
    def __init__(self, idGlobalClub, nombre, valorActual=0):
        self.idGlobalClub = idGlobalClub
        self.nombre = nombre
        self.valorActual = valorActual

    def returnWithCurrentValue(self, valorActual):
        aux = copy.copy(self)
        aux.valorActual = valorActual
        return aux

    def __str__(self):
        return "%s-%s (%s€)" % (self.idGlobalClub, self.nombre, self.valorActual)

    def __repr__(self):
        return self.__str__()

@dataclass
class Partido:
    idPartido: int
    division: str
    temporada: str
    jornada: int
    fecha: str
    idLocal: int
    localValue: str
    puntosLocal: int
    golesafavorlocal: int
    golesencontralocal: int
    idVisitante: int
    visitanteValue: str
    puntosVisitante: int
    golesafavorvisitante: int
    golesencontravisitante: int
    golesLocal: int
    golesVisitante: int

    def __str__(self):
        return "%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s" \
               % (self.idPartido, self.division, self.temporada, self.jornada, self.fecha,
                  self.idLocal, self.localValue, self.puntosLocal, self.golesafavorlocal, self.golesencontralocal,
                  self.idVisitante, self.visitanteValue, self.puntosVisitante, self.golesafavorvisitante, self.golesencontravisitante,
                  self.golesLocal, self.golesVisitante)
""" 
class Partido:
    def __init__(self, idPartido, division, temporada, jornada, fecha,
                 localId, localValue, puntosClasificacionLocal,
                 golesafavorlocal, golesencontralocal,
                 visitanteId, visitanteValue, puntosClasificacionVisitante,
                 golesafavorvisitante, golesencontravisitante,
                 goles_local, goles_visitante):
        self.idPartido = idPartido
        self.division = division
        self.temporada = temporada
        self.jornada = jornada
        self.fecha = fecha
        self.idLocal = localId
        self.localValue = localValue
        self.puntosLocal = puntosClasificacionLocal
        self.golesafavorlocal = golesafavorlocal
        self.golesencontralocal = golesencontralocal
        self.idVisitante = visitanteId
        self.visitanteValue = visitanteValue
        self.puntosVisitante = puntosClasificacionVisitante
        self.golesafavorvisitante = golesafavorvisitante
        self.golesencontravisitante = golesencontravisitante
        self.golesLocal = goles_local
        self.golesVisitante = goles_visitante

    def __str__(self):
        return "%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s" \
               % (self.idPartido, self.division, self.temporada, self.jornada, self.fecha,
                  self.idLocal, self.localValue, self.puntosLocal, self.golesafavorlocal, self.golesencontralocal,
                  self.idVisitante, self.visitanteValue, self.puntosVisitante, self.golesafavorvisitante, self.golesencontravisitante,
                  self.golesLocal, self.golesVisitante)
 """