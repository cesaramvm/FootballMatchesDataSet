import requests, json, os, pickle
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import UtilsAndGlobals as ut
from datetime import datetime, timedelta


class RefereesHelper:

    _instance = None  # Class variable to store the single instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RefereesHelper, cls).__new__(cls)
            cls._instance._init_singleton()
        return cls._instance

    def _init_singleton(self):
        self.SEASON_DIVISION_MATCHES_REFEREES = {}
        self.REFEREE_NAMES_TO_ID = {}
        self.CURRENT_REFEREE_ID = 1
        if ut.loadReferees:
            self._LOAD_REFEREES_VALUES()

    def getMatchRefereeAndResults(self, temporada, division, localGlobalId, visitanteGlobalId):
        ut.CHECK_KEY_EXISTANCE(temporada, self.SEASON_DIVISION_MATCHES_REFEREES, lambda: self._scrapeSeasonRefereesMatchesByLeague(temporada))
        matchId = str(localGlobalId) +"-"+ str(visitanteGlobalId)
        if matchId in self.SEASON_DIVISION_MATCHES_REFEREES[temporada][division]:
            return self.SEASON_DIVISION_MATCHES_REFEREES[temporada][division][matchId]
        return ("NullName", -1, "nullResult")
        

    def _CHECK_REFEREE_ID(self, refereeName):
        if refereeName in self.REFEREE_NAMES_TO_ID:
            return self.REFEREE_NAMES_TO_ID[refereeName]
        self.REFEREE_NAMES_TO_ID[refereeName] = self.CURRENT_REFEREE_ID
        self.CURRENT_REFEREE_ID = self.CURRENT_REFEREE_ID + 1
        return self.CURRENT_REFEREE_ID
        
    def _scrapeSeasonRefereesMatchesByLeague(self, añoTemporada):
        refereesNamesIDsAndHrefs=[]
        for division in [1,2]:
            print(Fore.RED + f"Scraping {añoTemporada}ª Referees"+Fore.RESET)
            url  = ut.REFEREES_URL % (division, añoTemporada)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                th_element =  soup.find('th', string='Árbitros')
                if th_element:
                    table_element = th_element.find_parent('table', class_='items')
                    elements = table_element.select('.hauptlink:not(.zentriert)')
                    for element in elements:
                        a_element = element.find('a')
                        if a_element:
                            arbitroName = a_element.text
                            arbitroHref = a_element['href']
                            arbitroId = self._CHECK_REFEREE_ID(arbitroName)
                            refereesNamesIDsAndHrefs.append([arbitroName, arbitroHref, arbitroId])

        datosPartidosyArbitrosPorDivision = {1:{}, 2:{}}
        for referee in refereesNamesIDsAndHrefs:
            refereeName = referee[0]
            refereeHref = referee[1]
            refereeId = referee[2]
            datosArbitro = self._scrapeRefereeMatches(refereeName, refereeHref, refereeId, añoTemporada)
            if any(datosPartidosyArbitrosPorDivision[key].keys() & datosArbitro[key].keys() for key in set(datosPartidosyArbitrosPorDivision) & set(datosArbitro)):
                print(str(datosArbitro))
                print(str(datosPartidosyArbitrosPorDivision))
                common_keys = set(datosPartidosyArbitrosPorDivision) & set(datosArbitro)
                repeated_keys = [key for key in common_keys if datosPartidosyArbitrosPorDivision[key].keys() & datosArbitro[key].keys()]
                print(repeated_keys)
                ut.RAISE("Imposible, partidos duplicados en la liga")
            datosPartidosyArbitrosPorDivision = {k: {**datosPartidosyArbitrosPorDivision.get(k, {}), **datosArbitro.get(k, {})} for k in set(datosPartidosyArbitrosPorDivision) | set(datosArbitro)}
        return datosPartidosyArbitrosPorDivision

    def _scrapeRefereeMatches(self, arbitroName, arbitroHref, arbitroId, añoTemporada):
        arbitroPartidosAmbasDivisiones = {}
        for division in [1,2]:
            partidosDivision = {}
            url = ut.REFEREES_MATCHES_URL % (arbitroHref, añoTemporada, division)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                laLigaHeadElement =  soup.find('div', class_='content-box-headline--logo')
                if laLigaHeadElement is not None:
                    table = laLigaHeadElement.find_next_sibling()
                    trs =  table.find_all('tr')
                    trs = trs[2:]
                    for tr in trs:
                        tdsEquipos = tr.find_all('td', class_="no-border-links")
                        equipoName1 = tdsEquipos[0].find('a').text if tdsEquipos[0].find('a') else None
                        equipoName2 = tdsEquipos[1].find('a').text if tdsEquipos[1].find('a') else None
                        equipoName12 = tdsEquipos[0].find('a').get('title', None) if tdsEquipos[0].find('a') else None
                        equipoName22= tdsEquipos[1].find('a').get('title', None) if tdsEquipos[1].find('a') else None
                        
                        resultado = tdsEquipos[1].find_next_sibling().find('a', class_='ergebnis-link').text

                        equipo1ID = ut.GET_GLOBAL_EQUIPO_ID_FROM_TRANSFERMARKT_NAME(equipoName1, equipoName12)
                        equipo2ID = ut.GET_GLOBAL_EQUIPO_ID_FROM_TRANSFERMARKT_NAME(equipoName2, equipoName22)
                        strPartido = str(equipo1ID) +"-"+ str(equipo2ID)
                        partidosDivision[strPartido] = [arbitroName, arbitroId,resultado]

                arbitroPartidosAmbasDivisiones[division] = partidosDivision
        return arbitroPartidosAmbasDivisiones

    def SAVE_REFEREES_VALUES(self, path=ut.SAVE_REFEREES_PATH):
        with open(path, 'wb') as file:
            pickle.dump(SEASON_DIVISION_MATCHES_REFEREES, file)

    def _LOAD_REFEREES_VALUES(self, path=ut.SAVE_REFEREES_PATH):
        if os.path.exists(path):
            global SEASON_DIVISION_MATCHES_REFEREES
            with open(path, 'rb') as file:
                loaded_dict = pickle.load(file)
            SEASON_DIVISION_MATCHES_REFEREES=loaded_dict