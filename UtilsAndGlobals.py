import sys
from Const import *
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

MARKET_INFO = dict()
firstMarketDate = datetime(2010, 8, 1).date()


def GET_MARKET_VALUE(division, equipoName, matchDate):
    f = open('marketFails.txt', 'a', encoding='utf-8')
    matchDate = datetime.strptime(matchDate, '%Y-%m-%d').date()
    #TODO ojo que esto al madrid y al barça a veces les pone 1.01 (millón) y no mil millon.
    if equipoName in MARKET_NAMES_CORRECTION:
        equipoName = MARKET_NAMES_CORRECTION[equipoName]
        if (matchDate > firstMarketDate):
            realMarketDate = min(FECHAS_VALORES, key=lambda sub: abs(sub.date() - matchDate))
            #f.write(f"Partido del {equipoName} el {matchDate}. Fecha market: {realMarketDate}. {division}ª división\n")
            if not realMarketDate in MARKET_INFO:
                MARKET_INFO[realMarketDate] = {}
            if not division in MARKET_INFO[realMarketDate]:
                MARKET_INFO[realMarketDate][division] = {}
            #f.write(f"  Hay que parsear el día: {realMarketDate} \n")
            teamsValues = dict()
            marketUrl = MARKET_URL[division] % realMarketDate.strftime("%Y-%m-%d")
            req = requests.get(marketUrl, headers={'User-Agent': 'Custom'})

            localMarketNodes = BeautifulSoup(req.text, "html.parser").find_all('td', {'class': 'hauptlink no-border-links'})
            for localNode in localMarketNodes:
                teamName = localNode.find("a")['title']
                teamValue = localNode.find_next_siblings()[1].find("a").string
                if(teamValue == "-"):
                    teamValue = -1
                else:
                    #Aqui justo a veces te entra algo como  "768,60 mill. €" o "1,06 mil mill. €"
                    teamValue = float(teamValue.split(" ")[0].replace(",","."))
                teamsValues[teamName] = teamValue

                MARKET_INFO[realMarketDate][division] = teamsValues


            
            if equipoName in MARKET_INFO[realMarketDate][division]:
                #f.write(f"  El valor es: {MARKET_INFO[realMarketDate][equipoName]}\n")
                return MARKET_INFO[realMarketDate][division][equipoName]
            else:
                found_keys = [key for key in MARKET_INFO[realMarketDate][division].keys() if equipoName in key]
                print(f"equipoName:{equipoName} foundkeys: {found_keys}")
                if found_keys:
                    return MARKET_INFO[realMarketDate][division][found_keys[0]]
    else:
        pass
    if not equipoName in MARKET_NAMES_CORRECTION:
        pass
        #f.write(f"  {equipoName} no está en MARKET_NAMES_CORRECTION\n")
    else:
        if matchDate > firstMarketDate and 'realMarketDate' in locals():
                f.write(f"  {equipoName} en el día REAL {realMarketDate} día del partido {matchDate}. Es de {division} división\n")
                f.write(f"  {MARKET_INFO[realMarketDate]}\n")
    f.close()
    return -1

def PRINT_MARKET_VALUES():
    print(MARKET_INFO)

def SAVE_MARKET_VALUES():
    import json
    with open(SAVE_MARKET_PATH, 'w') as json_obj:
        keys_as_string = json.dumps({k.strftime("%d/%m/%Y"): MARKET_INFO[k] for k in MARKET_INFO})
        json.dump(keys_as_string, json_obj, indent=4)

def LOAD_MARKET_VALUES():
    import json
    global MARKET_INFO
    MARKET_INFO = dict()
    try:
        with open(SAVE_MARKET_PATH, 'r') as load_obj:
            a = json.load(load_obj)
            """Convert the file string into a dictionary"""
            a = json.loads(a)
            a = {datetime.strptime(k, '%d/%m/%Y'): a[k] for k in a}
        MARKET_INFO=a
    except:
        pass


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
    

    fichero = open(fileName, 'w', encoding="utf-8")
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
                for partidoId in partidosJornada:
                    partido = partidosJornada[partidoId]
                    testString = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" \
                    % (str(partido.idPartido), str(partido.division), str(partido.temporada), str(partido.jornada), str(partido.matchDate),
                       str(partido.localName), str(partido.localId), str(partido.localMarketValue), str(partido.puntosLocal),
                       str(partido.golesafavorlocal), str(partido.golesencontralocal),
                       str(partido.visitanteName), str(partido.visitanteId), str(partido.visitanteMarketValue), str(partido.puntosVisitante),
                       str(partido.golesafavorvisitante), str(partido.golesencontravisitante),
                       str(partido.golesLocal), str(partido.golesVisitante), str(partido.golDiff))
                    fichero.write(testString)

    fichero.close()




    