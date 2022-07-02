#Autor original Ricardo Moya https://github.com/RicardoMoya/FootballMatchesDataSet
import copy

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


class Partido:
    def __init__(self, id_partido, division, temporada, jornada, fecha, idLocal,
                 idVisitante, puntosLocal, puntosVisitante, goles_local, goles_visitante):
        self.idPartido = id_partido
        self.temporada = temporada
        self.division = division
        self.jornada = jornada
        self.fecha = fecha
        self.idLocal = idLocal
        self.idVisitante = idVisitante
        self.golesLocal = goles_local
        self.golesVisitante = goles_visitante
        self.puntosLocal = puntosLocal
        self.puntosVisitante = puntosVisitante

    def __str__(self):
        return "%s::%s::%s::%s::%s::%s::%s::%s::%s" \
               % (self.idPartido, self.temporada, self.division, self.jornada, self.idLocal, self.idVisitante,
                  self.golesLocal, self.golesVisitante, self.fecha)
