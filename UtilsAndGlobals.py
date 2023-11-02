from Const import *
import UtilsAndGlobals as ut
import FootballClasses as fc
from colorama import Fore, Back, Style

loadFromFile = True
loadMarket = True
loadReferees = True

CURRENT_MATCH_ID = 1
CURRENT_TEAM_ID = 0
TEAM_NAMES_TO_ID = {}
IDs_TO_TEAM = {}
SAVE_SEASONS_PATH = 'TestSave.csv'
SAVE_MARKET_PATH = 'market_values.pickle'
SAVE_REFEREES_PATH = 'Referees.pickle'
ALL_SEASONS_INFO = {}

noTransferToGlobal = {}

def RAISE_IF(condition, error_message):
    if condition:
        RAISE(error_message)

def RAISE(error_message):
    raise Exception(error_message)
    
def CHECK_KEY_EXISTANCE(key, collection, newElement):
    if key in collection:
        return True
    collection[key] = newElement() if callable(newElement) else newElement
    return False

def GET_GLOBAL_EQUIPO_ID_FROM_TRANSFERMARKT_NAME(equipoName, alternateEquipoName):
    arrayPosibilidades = [equipoName, alternateEquipoName, TRANSFERMARKT_NAMES_TO_NORMAL.get(equipoName, None), TRANSFERMARKT_NAMES_TO_NORMAL.get(alternateEquipoName, None)]
    arrayIds = [GET_GLOBAL_EQUIPO_ID(element) for element in arrayPosibilidades if GET_GLOBAL_EQUIPO_ID(element, False) is not None]
    uniqueIds = set(arrayIds)
    if len(uniqueIds) == 0:
        raise ValueError("No equipo IDs found for {} - {}".format(equipoName, alternateEquipoName))
    elif len(uniqueIds) > 1:
        raise ValueError("Multiple equipo IDs found for {} - {}: {}".format(equipoName, alternateEquipoName, str(arrayIds)))
    else:
        equipoId = uniqueIds.pop()
        print("Single equipo ID:", equipoId)
        return equipoId
    
def SAVENOTTRANSFER():
    global noTransferToGlobal
    with open('noTransferToGlobal.txt', 'w', encoding='utf-8') as f:
        f.write(f"{noTransferToGlobal}")

def GET_GLOBAL_EQUIPO_ID(equipoName, alta=True):
    if equipoName in TEAM_NAMES_TO_ID:
        return TEAM_NAMES_TO_ID[equipoName]
    if alta:
        global CURRENT_TEAM_ID
        CURRENT_TEAM_ID = CURRENT_TEAM_ID + 1
        TEAM_NAMES_TO_ID[equipoName] = CURRENT_TEAM_ID
        equipo = fc.Equipo(CURRENT_TEAM_ID, equipoName)
        IDs_TO_TEAM[CURRENT_TEAM_ID] = equipo
        return CURRENT_TEAM_ID
    else:
        return None

def GET_CORRECTED_TEAM_NAME(equipo):
    ut.RAISE_IF(equipo not in NAMES_CORRECTION, f"{equipo} no está en la corrección")
    return NAMES_CORRECTION[equipo]

def ADD_SEASON_INFO(division, temporada, seasonInfo):
    ut.CHECK_KEY_EXISTANCE(division, ALL_SEASONS_INFO, {})
    ut.CHECK_KEY_EXISTANCE(temporada, ALL_SEASONS_INFO[division], seasonInfo)



def SAVE_MARKET_VALUES(path = SAVE_MARKET_PATH):
    marketHelper.SAVE_MARKET_VALUES(path)
    
def SAVE_REFEREES_VALUES(path = SAVE_REFEREES_PATH):
    refereesHelper.SAVE_REFEREES_VALUES(path)
    
def _writeHeaders(file, headersAndAttributes):
    file.write(';'.join(headersAndAttributes) + '\n')

def _writePartido(file, headersAndAttributes, partido):
    data = ';'.join(str(getattr(partido, attr, '')) for attr in headersAndAttributes)
    file.write(data + '\n')

def SAVE_ALL_SEASONS(fileName):
    fichero = open(fileName, 'w', encoding="utf-8")
    
    headersAndAttributes = ["idPartido", "division", "temporada", "jornada", "matchDate", "arbitroName", "arbitroId",
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


    

from RefereesHelper import RefereesHelper
from MarketHelper import MarketHelper
marketHelper = MarketHelper()
refereesHelper = RefereesHelper()