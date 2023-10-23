import sys
from Const import *
from MarketHelper import *
import UtilsAndGlobals as ut
import FootballClasses as fc
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style

CURRENT_MATCH_ID = 1
CURRENT_TEAM_ID = 1
TEAM_NAMES_TO_ID = dict()
IDs_TO_TEAM = dict()
SAVE_SEASONS_PATH = 'TestSave.csv'
SAVE_MARKET_PATH = 'market_values.json'
ALL_SEASONS_INFO = dict()

def CHECK_EQUIPO_ID(equipoName):
        if not equipoName in TEAM_NAMES_TO_ID:
            global CURRENT_TEAM_ID
            TEAM_NAMES_TO_ID[equipoName] = CURRENT_TEAM_ID
            equipo = fc.Equipo(CURRENT_TEAM_ID, equipoName)
            IDs_TO_TEAM[CURRENT_TEAM_ID] = equipo
            globalEquipoId = CURRENT_TEAM_ID
            CURRENT_TEAM_ID = CURRENT_TEAM_ID + 1
        else:
            globalEquipoId = TEAM_NAMES_TO_ID[equipoName]
        return globalEquipoId


# Funcion para sustituir el nombre de los equipos y unificarlos
def CHECK_EQUIPO_NAME(equipo):
    if equipo not in NAMES_CORRECTION:
        raise Exception(f"{equipo} no está en la corrección")
    else:
        equipo = NAMES_CORRECTION[equipo]
    return equipo


def ADD_SEASON_INFO(division, temporada, seasonInfo):
    if division not in ALL_SEASONS_INFO:
        ALL_SEASONS_INFO[division] = dict()
    if temporada not in ALL_SEASONS_INFO[division]:
        ALL_SEASONS_INFO[division][temporada] = seasonInfo

def SAVE_ALL_SEASONS(fileName):

#     fichero = open("test.txt", 'w')
#     fichero.write(str(ALL_SEASONS_INFO))
#     fichero.close()
    

    with open(fileName, 'w', encoding="utf-8") as fichero:
        fichero.write(  'idPartido;division;temporada;jornada;matchDate;'
                        'LocalName;EquipoLocalId;localMarketValue;PuntosClasiLocal;'
                        'GolesAFavorLocal;GolesEnContraLocal;'
                        'VisitanteName;EquipoVisitanteId;visitanteMarketValue;PuntosClasiVisitante;'
                        'GolesAFavorVisitante;GolesEnContraVisitante;'
                        'golesLocal;golesVisitante;golDiff\n')
        for division in ALL_SEASONS_INFO:
            for temporada in ALL_SEASONS_INFO[division]:
                datosTemporada = ALL_SEASONS_INFO[division][temporada]
                for jornada in datosTemporada.jornadas:
                    partidosJornada = datosTemporada.jornadas[jornada]
                    for partido_id, partido in partidosJornada.items():
                        
                        testString = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" \
                        % (str(partido.idPartido), str(partido.division), str(partido.temporada), str(partido.jornada), str(partido.matchDate),
                        str(partido.localName), str(partido.localId), str(partido.localMarketValue), str(partido.puntosLocal),
                        str(partido.golesafavorlocal), str(partido.golesencontralocal),
                        str(partido.visitanteName), str(partido.visitanteId), str(partido.visitanteMarketValue), str(partido.puntosVisitante),
                        str(partido.golesafavorvisitante), str(partido.golesencontravisitante),
                        str(partido.golesLocal), str(partido.golesVisitante), str(partido.golDiff))
                        fichero.write(testString)




    