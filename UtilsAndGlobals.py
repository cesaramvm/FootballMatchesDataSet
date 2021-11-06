import sys
from Const import *
from FutbolClasses import *

CURRENT_MATCH_ID = 0
CURRENT_TEAM_ID = 0
TEAM_NAMES_TO_ID = dict()
IDs_TO_TEAM = dict()

ALL_SEASONS_INFO = dict()

def CHECK_EQUIPO_ID(equipoName):
        if not equipoName in TEAM_NAMES_TO_ID:
            global CURRENT_TEAM_ID
            TEAM_NAMES_TO_ID[equipoName] = CURRENT_TEAM_ID
            equipo = Equipo(CURRENT_TEAM_ID, equipoName)
            IDs_TO_TEAM[CURRENT_TEAM_ID] = equipo
            globalEquipoId = CURRENT_TEAM_ID
            CURRENT_TEAM_ID = CURRENT_TEAM_ID + 1
        else:
            globalEquipoId = TEAM_NAMES_TO_ID[equipoName]
        return globalEquipoId


# Funcion para sustituir el nombre de los equipos y unificarlos
def CHECK_EQUIPO_NAME(equipo):
    if equipo not in NAMES_CORRECTION:
        print(equipo + " no está en la corrección")
        sys.exit(1)
    else:
        equipo = NAMES_CORRECTION[equipo]
    return equipo


def ADD_SEASON_INFO(division, temporada, seasonInfo):
    if division not in ALL_SEASONS_INFO:
        ALL_SEASONS_INFO[division] = dict()
    if temporada not in ALL_SEASONS_INFO[division]:
        ALL_SEASONS_INFO[division][temporada] = seasonInfo

def SAVE_ALL_SEASONS(fileName):
    fichero = open(fileName, 'w')
    fichero.write('idPartido;temporada;division;jornada;EquipoLocal;'
                  'EquipoVisitante;golesLocal;golesVisitante;fecha\n')
    for division in ALL_SEASONS_INFO:
        for temporada in ALL_SEASONS_INFO[division]:
            datosTemporada = ALL_SEASONS_INFO[division][temporada]
            for jornada in datosTemporada.jornadas:
                partidosJornada = datosTemporada.jornadas[jornada]
                for partidoId in partidosJornada:
                    partido = partidosJornada[partidoId]
                    testString = '%s;%s;%s;%s;%s;%s;%s;%s;%s\n' % (str(partido.idPartido), str(partido.temporada), str(partido.division), str(partido.jornada), str(partido.local.nombre), str(partido.visitante.nombre), str(partido.golesLocal), str(partido.golesVisitante), str(partido.fecha))
                    fichero.write(testString)

    fichero.close()
    # print("OJO QUE ESTÁ SIN HACER EL SAVEINFO")
    # for value in partidos.values():
    #     fichero.write('%s\n' % str(value))
