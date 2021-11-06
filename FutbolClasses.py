#Autor original Ricardo Moya https://github.com/RicardoMoya/FootballMatchesDataSet
import copy

class Temporada:
    def __init__(self, año):
        self.año = año
        self.teams = []
        self.jornadas = []

class Equipo:
    def __init__(self, idGlobalClub, nombre, valorActual = 0):
        self.idGlobalClub = idGlobalClub
        self.nombre = nombre
        self.valorActual = valorActual

    def assignValorActual(self, valorActual):
        aux = copy.copy(self)
        aux.valorActual = valorActual
        return aux

    def __str__(self):
        return "%s-%s (%s€)" % (self.idGlobalClub, self.nombre, self.valorActual)

    def __repr__(self):
        return self.__str__()


class Partido:
    def __init__(self, id_partido, division, temporada,  jornada, fecha, local,
                 visitante, goles_local, goles_visitante, puntosLocal, puntosVisitante):
        self.idPartido = id_partido
        self.temporada = temporada
        self.division = division
        self.jornada = jornada
        self.fecha = fecha
        self.local = local
        self.visitante = visitante
        self.golesLocal = goles_local
        self.golesVisitante = goles_visitante
        self.puntosLocal = puntosLocal
        self.puntosVisitante = puntosVisitante
        self.objective = "1" if goles_local>goles_visitante else ("X" if goles_local==goles_visitante else "2")

    def __str__(self):
        return "%s::%s::%s::%s::%s::%s::%s::%s::%s" \
               % (self.idPartido, self.temporada, self.division, self.jornada, self.local, self.visitante,
                  self.golesLocal, self.golesVisitante, self.fecha)
