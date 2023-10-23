import requests, json, os
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import UtilsAndGlobals as ut
from datetime import datetime, timedelta

firstMarketDate = datetime.now().date()
notInCorrectionTeams = set()

MARKET_INFO = {}

def scrapeMarketDatesToDictionary(division):
    print(Fore.RED + f"Scraping {division}ª Market Dates"+Fore.RESET)
    url = ut.MARKET_URL[division]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        select_element = soup.find('select', {'class': 'chzn-select'})
        if select_element:
            option_values = {datetime.strptime(option['value'], "%Y-%m-%d").date(): {} for option in select_element.find_all('option')}
            SET_FIRST_MARKET_DATE(option_values)
            return option_values
    raise Exception("No scraping Market Dates Found")

def scrapeMarketValues(division, realMarketDate):
    print(Fore.MAGENTA + f"Scraping {division}ª Market Values ON {realMarketDate}"+Fore.RESET)
    teamsValues = {}
    marketUrl = ut.MARKET_URL[division] % realMarketDate.strftime("%Y-%m-%d")
    req = requests.get(marketUrl, headers={'User-Agent': 'Custom'})

    localMarketNodes = BeautifulSoup(req.text, "html.parser").find_all('td', {'class': 'hauptlink no-border-links'})
    for localNode in localMarketNodes:
        teamName = localNode.find("a")['title']
        teamValue = localNode.find_next_siblings()[1].find("a").string
        if(teamValue == "-"):
            teamValue = -1
        else:
            #TODO
            #Aqui justo a veces te entra algo como  "768,60 mill. €" o "1,06 mil mill. €"
            teamValue = float(teamValue.split(" ")[0].replace(",","."))
        teamsValues[teamName] = teamValue
    return teamsValues

def getTeamsMarketValue(division, matchDate, localName, visitanteName):
    return [getMarketValue(division, localName, matchDate),getMarketValue(division, visitanteName, matchDate)]

def getMarketValue(division, equipoName, matchDate):
    matchDate = datetime.strptime(matchDate, '%Y-%m-%d').date()
    ut.CHECK_KEY_EXISTANCE(division, MARKET_INFO, lambda: scrapeMarketDatesToDictionary(division))
    if equipoName not in ut.MARKET_NAMES_CORRECTION:
        notInCorrectionTeams.add(equipoName)
        return -1
    if matchDate < firstMarketDate:
        return -1
        
    equipoName = ut.MARKET_NAMES_CORRECTION[equipoName]
    realMarketDate = min(MARKET_INFO[division], key=lambda date: abs((date - matchDate) if ((date - matchDate).days)<=0 else timedelta(days=9999)))
    if not MARKET_INFO[division][realMarketDate]:
        MARKET_INFO[division][realMarketDate] = scrapeMarketValues(division, realMarketDate)
        SAVE_MARKET_VALUES(ut.SAVE_MARKET_PATH)
    if equipoName not in MARKET_INFO[division][realMarketDate]:
        return -1
        found_keys = [key for key in MARKET_INFO[realMarketDate][division].keys() if equipoName in key]
        print(f"equipoName:{equipoName} foundkeys: {found_keys}")
        if found_keys:
            return MARKET_INFO[realMarketDate][division][found_keys[0]]
    return MARKET_INFO[division][realMarketDate][equipoName]

def printMarketValues():
    print(MARKET_INFO)

import pickle
def SAVE_MARKET_VALUES(path):
    with open(path, 'wb') as file:
        pickle.dump(MARKET_INFO, file)

def LOAD_MARKET_VALUES(path):
    if os.path.exists(path):
        global MARKET_INFO
        with open(path, 'rb') as file:
            loaded_dict = pickle.load(file)
        MARKET_INFO=loaded_dict

        dates = set()
        if 1 in MARKET_INFO:
            dates.update(MARKET_INFO[1].keys())
        if 2 in MARKET_INFO:
            dates.update(MARKET_INFO[2].keys())
        SET_FIRST_MARKET_DATE(dates)

def SET_FIRST_MARKET_DATE(collection):
    global firstMarketDate
    earliest_date = min(collection)
    if earliest_date < firstMarketDate:
        firstMarketDate = earliest_date

    print(firstMarketDate)



def SAVE_NOT_CORRECTED_NAMES():
    with open('marketFails.txt', 'w', encoding='utf-8') as f:
        f.write(f"{notInCorrectionTeams}")