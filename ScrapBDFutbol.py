#Autor original Ricardo Moya https://github.com/RicardoMoya/FootballMatchesDataSet
import json

from bs4 import BeautifulSoup
from FutbolClasses import Partido
import requests
import re
import Const
import time


temporada = dict()

# Guardo los partidos de futbol con un id
partidos = dict()


# Guardo los equipos de futbol con su id y su nombre
idToEquipoDict = dict()
equipoToIdDict = dict()
equipoCount = 0

# Contador de Partidos
contador = 0


def getInfo():
    return scrape1y2()

# Devuelvo un diccionario con todos los partidos de
# futbol de todas las temporadas
def scrape1y2():
    # Genero las URLS y scrapeo los datos
    for season in Const.TEMPORADAS:
        print("****  PROCESANDO TEMPORADA %s ****" % season)
        # Construyo las URLs
        resultScrapePrimera = scrapeLeague(Const.URL_PRIMERA, season, temporada[season]["1"])
        temporada[season] = {"1":resultScrapePrimera}

        resultScrapeSegunda = scrapeLeague(Const.URL_SEGUNDA, season, temporada[season]["1"])
        temporada[season] = {"2": resultScrapeSegunda}


    return partidos

def scrapeLeague(leagueUrlConst, season, saveData):
    url = leagueUrlConst % season
    req = requests.get(url)
    soupReq = BeautifulSoup(req.text, "html.parser")
    seasonData = str(soupReq.find('div', {'id': 'resultats'}))
    findEquipos(seasonData)
    findPartidos(seasonData, season, 1)

# Funcion para sustituir el nombre de los equipos y unificarlos
def replaceEquipos(equipo):
    equipo = equipo.replace('Deportivo de La Coruña', 'Deportivo')
    equipo = equipo.replace('Barcelona Atletic', 'Barcelona B')
    return equipo


# Inserto los equipos nuevos en el diccionario
def findEquipos(str_resultados):
    global equipoCount
    match = re.findall(r'SE\[\d{0,100}\]=\".*?\";', str_resultados)
    for mat in match:
        mat = re.sub(r'SE.*?="', '', mat)
        mat = mat.replace('";', '')
        sp = mat.split('|')
        #Todo guardar en un diccionario temporal
        currentEquipoId = sp[0]
        equipo = sp[1]

        if not equipo in equipoToIdDict:
            idToEquipoDict[equipoCount] = equipo
            equipoToIdDict[equipo] = equipoCount
            equipoCount = equipoCount + 1


# Obtengo una lista con los partidos de futbol de una temporada
def findPartidos(str_partidos, temporada, division):
    global contador

    matches = re.findall(r'SP\[\d{0,100}\]\[\d{0,100}\]=\".*?\";', str_partidos)
    matches = re.findall(r'SP\[\d{0,100}\].push\(.*\);', str_partidos)
    for matchData in matches:
        jornada = re.findall(r'SP\[.*?]', matchData)[0].replace('SP[', '').replace(']', '')
        jsonInfo = json.loads(re.findall(r'\{.*\}', matchData)[0])
        dia = jsonInfo.get("d")
        eq1Id = int(jsonInfo.get("a1"))
        eq2Id = int(jsonInfo.get("a2"))
        score1 = int(jsonInfo.get("g1"))
        score2 = int(jsonInfo.get("g2"))
        contador += 1
        local = replaceEquipos(idToEquipoDict[eq1Id])
        visitante = replaceEquipos(idToEquipoDict[eq2Id])
        partidos[contador] = Partido(contador, temporada, division, jornada, local,
                                     visitante, score1, score2, dia)

    return partidos




# Devuelvo el valor del contador
def get_contador():
    return contador
