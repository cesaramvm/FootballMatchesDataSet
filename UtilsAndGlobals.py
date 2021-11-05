import sys
from Const import *

CURRENT_MATCH_ID = 1
CURRENT_TEAM_ID = 1
ALL_TEAMS_TO_ID = dict()
ALL_IDS_TO_TEAM = dict()

ALL_SEASONS_INFO = dict()

def ADD_SEASON_INFO(division, temporada, seasonInfo):
    if division not in ALL_SEASONS_INFO:
        ALL_SEASONS_INFO[division] = dict()
    if temporada not in ALL_SEASONS_INFO[division]:
        ALL_SEASONS_INFO[division][temporada] = seasonInfo

def SAVE_ALL_SEASONS(fileName):
    fichero = open(fileName, 'w')
    fichero.write('idPartido::temporada::division::jornada::EquipoLocal::'
                  'EquipoVisitante::golesLocal::golesVisitante::fecha\n')
    print("OJO QUE ESTÁ SIN HACER EL SAVEINFO")
    # for value in partidos.values():
    #     fichero.write('%s\n' % str(value))


# Funcion para sustituir el nombre de los equipos y unificarlos
def CHECK_EQUIPO_NAME(equipo):
    if equipo not in NAMES_CORRECTION:
        print(equipo + " no está en la corrección")
        sys.exit(1)
    else:
        equipo = NAMES_CORRECTION[equipo]
    return equipo
