import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import UtilsAndGlobals as ut
from datetime import datetime

MARKET_INFO = dict()
firstMarketDate = datetime.now().date()

FECHAS_VALORES = {1:[],2:[]}

def scrapeMarketDates(division):
    print("SCRAPING DIVISION " + str(division))
    global firstMarketDate
    url = ut.MARKET_URL[division]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        select_element = soup.find('select', {'class': 'chzn-select'})
        if select_element:
            option_values = [datetime.strptime(option['value'], "%Y-%m-%d").date() for option in select_element.find_all('option')]
            earliest_date = min(option_values)
            if earliest_date < firstMarketDate:
                firstMarketDate = earliest_date
            return option_values
    raise Exception("No scraping Market Dates Found")

def getTeamsMarketValue(division, matchDate, localName, visitanteName):
    return [getMarketValue(division, localName, matchDate),getMarketValue(division, visitanteName, matchDate)]

def getMarketValue(division, equipoName, matchDate):
    return -1
    if len(FECHAS_VALORES[division]) == 0:
        FECHAS_VALORES[division] = scrapeMarketDates(division)
    f = open('marketFails.txt', 'a', encoding='utf-8')
    matchDate = datetime.strptime(matchDate, '%Y-%m-%d').date()
    #TODO ojo que esto al madrid y al barça a veces les pone 1.01 (millón) y no mil millon.
    if equipoName in ut.MARKET_NAMES_CORRECTION:
        equipoName = ut.MARKET_NAMES_CORRECTION[equipoName]
        if (matchDate > firstMarketDate):
            realMarketDate = min(FECHAS_VALORES[division], key=lambda sub: abs(sub.date() - matchDate))
            #f.write(f"Partido del {equipoName} el {matchDate}. Fecha market: {realMarketDate}. {division}ª división\n")
            if not realMarketDate in MARKET_INFO:
                MARKET_INFO[realMarketDate] = {}
            if not division in MARKET_INFO[realMarketDate]:
                MARKET_INFO[realMarketDate][division] = {}
            #f.write(f"  Hay que parsear el día: {realMarketDate} \n")
            teamsValues = dict()
            marketUrl = ut.MARKET_URL[division] % realMarketDate.strftime("%Y-%m-%d")
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
    if not equipoName in ut.MARKET_NAMES_CORRECTION:
        pass
        #f.write(f"  {equipoName} no está en MARKET_NAMES_CORRECTION\n")
    else:
        if matchDate > firstMarketDate and 'realMarketDate' in locals():
                f.write(f"  {equipoName} en el día REAL {realMarketDate} día del partido {matchDate}. Es de {division} división\n")
                f.write(f"  {MARKET_INFO[realMarketDate]}\n")
    f.close()
    return -1

def printMarketValues():
    print(MARKET_INFO)

def SAVE_MARKET_VALUES():
    import json
    with open(ut.SAVE_MARKET_PATH, 'w') as json_obj:
        keys_as_string = json.dumps({k.strftime("%d/%m/%Y"): MARKET_INFO[k] for k in MARKET_INFO})
        json.dump(keys_as_string, json_obj, indent=4)

def LOAD_MARKET_VALUES():
    import json
    global MARKET_INFO
    MARKET_INFO = dict()
    try:
        with open(ut.SAVE_MARKET_PATH, 'r') as load_obj:
            a = json.load(load_obj)
            """Convert the file string into a dictionary"""
            a = json.loads(a)
            a = {datetime.strptime(k, '%d/%m/%Y'): a[k] for k in a}
        MARKET_INFO=a
    except:
        pass

