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
TEAM_NAMES_TO_ID = {}
IDs_TO_TEAM = {}
SAVE_SEASONS_PATH = 'TestSave.csv'
SAVE_MARKET_PATH = 'market_values.json'
ALL_SEASONS_INFO = {}

def CHECK_KEY_EXISTANCE(key, collection, newElement):
    if not key in collection:
        if callable(newElement):
            collection[key] = newElement()
        else:
            collection[key] = newElement
        return False
    return True

def CHECK_EQUIPO_ID(equipoName):
        if equipoName not in TEAM_NAMES_TO_ID:
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
    ut.CHECK_KEY_EXISTANCE(division, ALL_SEASONS_INFO, {})
    ut.CHECK_KEY_EXISTANCE(temporada, ALL_SEASONS_INFO[division], seasonInfo)


def _writeHeaders(file, headersAndAttributes):
    file.write(';'.join(headersAndAttributes) + '\n')

def _writePartido(file, headersAndAttributes, partido):
    data = ';'.join(str(getattr(partido, attr, '')) for attr in headersAndAttributes)
    file.write(data + '\n')

def SAVE_ALL_SEASONS(fileName):
    fichero = open(fileName, 'w', encoding="utf-8")
    
    # Define the column names for the header and partido attributes
    headersAndAttributes = ["idPartido", "division", "temporada", "jornada", "matchDate",
                            "localName", "localId", "localMarketValue", "puntosLocal",
                            "golesafavorlocal", "golesencontralocal", "visitanteName", "visitanteId",
                            "visitanteMarketValue", "puntosVisitante", "golesafavorvisitante", "golesencontravisitante",
                            "golesLocal", "golesVisitante", "golDiff"]
    _writeHeaders(fichero, headersAndAttributes)
    flat_partidos = [partido for division in ALL_SEASONS_INFO for temporada in ALL_SEASONS_INFO[division]
                    for jornada in ALL_SEASONS_INFO[division][temporada].jornadas
                    for partido in ALL_SEASONS_INFO[division][temporada].jornadas[jornada].values()]
    
    for partido in flat_partidos:
        _writePartido(fichero, headersAndAttributes, partido)

    fichero.close()