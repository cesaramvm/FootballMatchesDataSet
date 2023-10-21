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
    division: int
    temporada: str
    jornada: int
    fecha: str
    idLocal: int
    localName: str
    localMarketValue: str
    puntosLocal: int
    golesafavorlocal: int
    golesencontralocal: int
    idVisitante: int
    visitanteName: str
    visitanteMarketValue: str
    puntosVisitante: int
    golesafavorvisitante: int
    golesencontravisitante: int
    golesLocal: int
    golesVisitante: int
    golDiff: int

    def __str__(self):
        return "%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s::%s" \
               % (self.idPartido, self.division, self.temporada, self.jornada, self.fecha,
                  self.idLocal, self.localValue, self.puntosLocal, self.golesafavorlocal, self.golesencontralocal,
                  self.idVisitante, self.visitanteValue, self.puntosVisitante, self.golesafavorvisitante, self.golesencontravisitante,
                  self.golesLocal, self.golesVisitante, self.golDiff)
