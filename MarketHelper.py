import requests, json, os, pickle
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import UtilsAndGlobals as ut
from datetime import datetime, timedelta

class MarketHelper:
    _instance = None  # Class variable to store the single instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MarketHelper, cls).__new__(cls)
            cls._instance._init_singleton()
        return cls._instance

    def _init_singleton(self):
        self.firstMarketDate = datetime.now().date()
        self.notInCorrectionTeams = set()
        self.notInMarketTeams = set()
        self.MARKET_INFO = {}
        if ut.loadMarket:
            self._LOAD_MARKET_VALUES()
        ut.CHECK_KEY_EXISTANCE(1, self.MARKET_INFO, lambda: self._scrapeMarketDatesToDictionary(1))
        ut.CHECK_KEY_EXISTANCE(2, self.MARKET_INFO, lambda: self._scrapeMarketDatesToDictionary(2))

    def _scrapeMarketDatesToDictionary(self, division):
        print(Fore.RED + f"Scraping {division}ª Market Dates"+Fore.RESET)
        url = ut.MARKET_URL % (division,"")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            select_element = soup.find('select', {'class': 'chzn-select'})
            if select_element:
                option_values = {datetime.strptime(option['value'], "%Y-%m-%d").date(): {} for option in select_element.find_all('option')}
                self._SET_FIRST_MARKET_DATE(option_values)
                return option_values
        ut.RAISE("No scraping Market Dates Found")

    def scrapeMarketTeamValues(self, division, realMarketDate):
        print(Fore.MAGENTA + f"Scraping {division}ª Market Values ON {realMarketDate}"+Fore.RESET)
        teamsValues = {}
        marketUrl = ut.MARKET_URL % (division, realMarketDate.strftime("%Y-%m-%d"))
        req = requests.get(marketUrl, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/537.36'})
        localMarketNodes = BeautifulSoup(req.text, "html.parser").find_all('td', {'class': 'hauptlink no-border-links'})
        for localNode in localMarketNodes:
            teamName = localNode.find("a")['title']
            teamValueText = localNode.find_next_siblings()[1].find("a").string
            teamsValues[teamName] = -1 if teamValueText == "-" else float(teamValueText.split(" ")[0].replace(",", ".")) * 1000 if "mil mill." in teamValueText else float(teamValueText.split(" ")[0].replace(",", "."))
        return teamsValues

    def getTeamsMarketValue(self, division, matchDate, localName, visitanteName):
        return [self._getMarketValue(division, localName, matchDate),self._getMarketValue(division, visitanteName, matchDate)]

    def _getMarketValue(self, division, equipoName, matchDate):
        matchDate = datetime.strptime(matchDate, '%Y-%m-%d').date()
        if matchDate < self.firstMarketDate:
            return -1

        realMarketDate = min(self.MARKET_INFO[division], key=lambda date: abs((date - matchDate) if ((date - matchDate).days)<=0 else timedelta(days=9999)))
        if not self.MARKET_INFO[division][realMarketDate]:
            self.MARKET_INFO[division][realMarketDate] = self.scrapeMarketTeamValues(division, realMarketDate)



        if equipoName not in ut.NAMES_TO_TRANSFERMARKT_NAMES:
            self.notInCorrectionTeams.add(equipoName)
            equipoNames = equipoName
        else:
            equipoNames = ut.NAMES_TO_TRANSFERMARKT_NAMES[equipoName]
        equipoNames = equipoNames if isinstance(equipoNames, list) else [equipoNames]
        
        results = []
        for equipoName in equipoNames:
             for key, market_list in self.MARKET_INFO.items():
                if equipoName in market_list[realMarketDate]:
                    results.append((equipoName, key))
                    ut.RAISE_IF(equipoName not in self.MARKET_INFO[key][realMarketDate], "WTF")

        print(results)

        #TODO aqui quizás hacer la búsqueda y que salgan literalmente la division en la que está y el nombre que utiliza



        if equipoName not in self.MARKET_INFO[division][realMarketDate]:
            backupDivision = 1 if division==2 else 2
            if not self.MARKET_INFO[backupDivision][realMarketDate]:
                self.MARKET_INFO[backupDivision][realMarketDate] = self.scrapeMarketTeamValues(backupDivision, realMarketDate)
            if equipoName in self.MARKET_INFO[backupDivision][realMarketDate]:
                return self._getMarketValue(backupDivision, equipoName, str(matchDate))
            found_keys = [key for key in self.MARKET_INFO[division][realMarketDate].keys() if equipoName in key]
            found_keys2 = [key for key in self.MARKET_INFO[backupDivision][realMarketDate].keys() if equipoName in key]
            
            if not found_keys and not found_keys2:
                self.notInMarketTeams.add(equipoName)
                return -1
            else:
                if not found_keys:
                    found_keys = found_keys2
                    division = backupDivision
                #print(f"equipoName:{equipoName} foundkeys: {found_keys} in div: {division}")
            backupEquipoName = equipoName
            equipoName = found_keys[0]
            print(f"oldequipoName:{backupEquipoName} - new equipoName:{equipoName} ")
        return self.MARKET_INFO[division][realMarketDate][equipoName]

    def _SET_FIRST_MARKET_DATE(self, collection):
        earliest_date = min(collection)
        if earliest_date < self.firstMarketDate:
            self.firstMarketDate = earliest_date

    def SAVE_MARKET_VALUES(self, path=ut.SAVE_MARKET_PATH):
        with open(path, 'wb') as file:
            pickle.dump(self.MARKET_INFO, file)
        with open('uncorrectedMarketNames.txt', 'w', encoding='utf-8') as f:
            f.write(f"{self.notInCorrectionTeams}")
        with open('notInMarketNames.txt', 'w', encoding='utf-8') as f:
            f.write(f"{self.notInMarketTeams}")

    def _LOAD_MARKET_VALUES(self, path=ut.SAVE_MARKET_PATH):
        if os.path.exists(path):
            with open(path, 'rb') as file:
                loaded_dict = pickle.load(file)
            self.MARKET_INFO=loaded_dict

            dates = set()
            if 1 in self.MARKET_INFO:
                dates.update(self.MARKET_INFO[1].keys())
            if 2 in self.MARKET_INFO:
                dates.update(self.MARKET_INFO[2].keys())
            self._SET_FIRST_MARKET_DATE(dates)