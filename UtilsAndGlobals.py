import sys
from Const import *
import FootballClasses as fc
import requests
from bs4 import BeautifulSoup

CURRENT_MATCH_ID = 1
CURRENT_TEAM_ID = 1
TEAM_NAMES_TO_ID = dict()
IDs_TO_TEAM = dict()


ALL_SEASONS_INFO = dict()

MARKET_INFO = dict()
firstMarketDate = datetime(2010, 8, 1)

def GET_MARKET_VALUE(equipoName, matchDate):
    #TODO ojo que esto al madrid y al barça a veces les pone 1.01 (millón) y no mil millon.
    if equipoName in MARKET_NAMES_CORRECTION:
        equipoName = MARKET_NAMES_CORRECTION[equipoName]
        if (matchDate > firstMarketDate):
            realMarketDate = min(FECHAS_VALORES, key=lambda sub: abs(sub - matchDate))
            if(realMarketDate in MARKET_INFO):
                return MARKET_INFO[realMarketDate][equipoName]
            else:
                teamsValues = dict()
                for division in range(1, 3):
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

                    MARKET_INFO[realMarketDate] = teamsValues
                return MARKET_INFO[realMarketDate][equipoName]
    else:
        return -1

def PRINT_MARKET_VALUES():
    print(MARKET_INFO)

def SAVE_MARKET_VALUES():
    import json
    with open('market_values.json', 'w') as json_obj:
        keys_as_string = json.dumps({k.strftime("%d/%m/%Y"): MARKET_INFO[k] for k in MARKET_INFO})
        json.dump(keys_as_string, json_obj, indent=4)

def LOAD_MARKET_VALUES():
    import json
    global MARKET_INFO
    MARKET_INFO = dict()
    try:
        with open('market_values.json', 'r') as load_obj:
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
    fichero.write(  'idPartido;division;temporada;jornada;fecha;'
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
                    % (str(partido.idPartido), str(partido.division), str(partido.temporada), str(partido.jornada), str(partido.fecha),
                       str(IDs_TO_TEAM[partido.idLocal].nombre), str(partido.idLocal), str(partido.localMarketValue), str(partido.puntosLocal),
                       str(partido.golesafavorlocal), str(partido.golesencontralocal),
                       str(IDs_TO_TEAM[partido.idVisitante].nombre), str(partido.idVisitante), str(partido.visitanteMarketValue), str(partido.puntosVisitante),
                       str(partido.golesafavorvisitante), str(partido.golesencontravisitante),
                       str(partido.golesLocal), str(partido.golesVisitante), str(partido.golDiff))
                    fichero.write(testString)

    fichero.close()


def LOAD_ALL_SEASONS(fileName):
    global ALL_SEASONS_INFO
    ALL_SEASONS_INFO = dict()
    
    with open(fileName, 'r') as file:
        # Skip the header line
        next(file)
        for line in file:
            parts = line.strip().split(';')
            partido = fc.Partido(*parts)
            print(partido.division)
            print(type(partido.division))
            if partido.division not in ALL_SEASONS_INFO:
                ALL_SEASONS_INFO[partido.division] = {}
            if partido.temporada not in ALL_SEASONS_INFO[partido.division]:
                ALL_SEASONS_INFO[partido.division][partido.temporada] = {}

            # Add the partido object to the dictionary
            ALL_SEASONS_INFO[partido.division][partido.temporada][partido.jornada] = partido

    print(ALL_SEASONS_INFO.keys())