import requests, json, os, pickle
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import UtilsAndGlobals as ut
from datetime import datetime, timedelta

firstMarketDate = datetime.now().date()
notInCorrectionTeams = set()
notInMarketTeams = set()

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

def scrapeMarketTeamValues(division, realMarketDate):
    print(Fore.MAGENTA + f"Scraping {division}ª Market Values ON {realMarketDate}"+Fore.RESET)
    teamsValues = {}
    marketUrl = ut.MARKET_URL[division] % realMarketDate.strftime("%Y-%m-%d")
    req = requests.get(marketUrl, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/537.36'})

    localMarketNodes = BeautifulSoup(req.text, "html.parser").find_all('td', {'class': 'hauptlink no-border-links'})
    for localNode in localMarketNodes:
        teamName = localNode.find("a")['title']
        teamValueText = localNode.find_next_siblings()[1].find("a").string
        if(teamValueText == "-"):
            teamValue = -1
        else:
            teamValue = float(teamValueText.split(" ")[0].replace(",","."))
            if "mil mill." in teamValueText:
                teamValue *= 1000
        teamsValues[teamName] = teamValue
    return teamsValues

def getTeamsMarketValue(division, matchDate, localName, visitanteName):
    return [getMarketValue(division, localName, matchDate),getMarketValue(division, visitanteName, matchDate)]

def getMarketValue(division, equipoName, matchDate):
    ut.CHECK_KEY_EXISTANCE(division, MARKET_INFO, lambda: scrapeMarketDatesToDictionary(division))
    matchDate = datetime.strptime(matchDate, '%Y-%m-%d').date()
    if matchDate < firstMarketDate:
        return -1
    if equipoName not in ut.MARKET_NAMES_CORRECTION:
        notInCorrectionTeams.add(equipoName)
    else:
        equipoName = ut.MARKET_NAMES_CORRECTION[equipoName]
    realMarketDate = min(MARKET_INFO[division], key=lambda date: abs((date - matchDate) if ((date - matchDate).days)<=0 else timedelta(days=9999)))
    if not MARKET_INFO[division][realMarketDate]:
        MARKET_INFO[division][realMarketDate] = scrapeMarketTeamValues(division, realMarketDate)
    if equipoName not in MARKET_INFO[division][realMarketDate]:
        backupDivision = 1 if division==2 else 2
        ut.CHECK_KEY_EXISTANCE(backupDivision, MARKET_INFO, lambda: scrapeMarketDatesToDictionary(backupDivision))        
        if not MARKET_INFO[backupDivision][realMarketDate]:
            MARKET_INFO[backupDivision][realMarketDate] = scrapeMarketTeamValues(backupDivision, realMarketDate)
        if equipoName in MARKET_INFO[backupDivision][realMarketDate]:
            value = getMarketValue(backupDivision, equipoName, str(matchDate))
            #print(f"equipoName:{equipoName} encontrado en otra div: with value {value}")
            return value
        found_keys = [key for key in MARKET_INFO[division][realMarketDate].keys() if equipoName in key]
        found_keys2 = [key for key in MARKET_INFO[backupDivision][realMarketDate].keys() if equipoName in key]
        
        if not found_keys and not found_keys2:
            notInMarketTeams.add(equipoName)
            return -1
        else:
            if not found_keys:
                found_keys = found_keys2
                division = backupDivision
            print(f"equipoName:{equipoName} foundkeys: {found_keys} in div: {division}")
        backupEquipoName = equipoName
        equipoName = found_keys[0]
        print(f"oldequipoName:{backupEquipoName} - new equipoName:{equipoName} ")
    return MARKET_INFO[division][realMarketDate][equipoName]

def SET_FIRST_MARKET_DATE(collection):
    global firstMarketDate
    earliest_date = min(collection)
    if earliest_date < firstMarketDate:
        firstMarketDate = earliest_date

def SAVE_MARKET_VALUES(path):
    with open(path, 'wb') as file:
        pickle.dump(MARKET_INFO, file)
    with open('uncorrectedMarketNames.txt', 'w', encoding='utf-8') as f:
        f.write(f"{notInCorrectionTeams}")
    with open('notInMarketNames.txt', 'w', encoding='utf-8') as f:
        f.write(f"{notInMarketTeams}")

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