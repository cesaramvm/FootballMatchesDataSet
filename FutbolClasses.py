#Autor original Ricardo Moya https://github.com/RicardoMoya/FootballMatchesDataSet

import time
import datetime

class Temporada:
    def __init__(self, año):
        self.año = año
        self.teams = []
        self.jornadas = []

class Equipo:
    def __init__(self, id_club, nombre, valor):
        self.id_club = id_club
        self.nombre = nombre
        self.valorActual = valor

    def __str__(self):
        return "%s - %s - %s" % (self.id_club, self.nombre, self.valorActual)


class Partido:
    def __init__(self, id_partido, division,temporada,  jornada, local,
                 visitante, goles_local, goles_visitante, fecha):
        self.idPartido = id_partido
        self.temporada = temporada
        self.division = division
        self.jornada = jornada
        self.local = local
        self.visitante = visitante
        self.golesLocal = goles_local
        self.golesVisitante = goles_visitante
        self.fecha = fecha

    def __str__(self):
        return "%s::%s::%s::%s::%s::%s::%s::%s::%s" \
               % (self.idPartido, self.temporada, self.division, self.jornada, self.local, self.visitante,
                  self.golesLocal, self.golesVisitante, self.fecha)
