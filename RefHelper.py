import requests, json, os, pickle
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import UtilsAndGlobals as ut
from datetime import datetime, timedelta

firstMarketDate = datetime.now().date()
notInCorrectionTeams = set()
notInMarketTeams = set()

MARKET_INFO = {}

def scrapeSeasonReferees(division, añoTemporada):
    refereesNamesAndHrefs=[]
    print(Fore.RED + f"Scraping {añoTemporada}ª Referees"+Fore.RESET)
    url  = ut.REFEREES_URL % (division, añoTemporada)
    print(url)
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
                    scrapeRefereeMatches(division, añoTemporada, arbitroName, arbitroHref)
                    #refereesNamesAndHrefs.append([arbitro, arbitroHref])

            return refereesNamesAndHrefs
    raise Exception("No referees Found")

def scrapeRefereeMatches(division, añoTemporada, arbitroName, arbitroHref):
    currentYear = str(datetime.today().year)
    season = 1
    url = ut.REFEREES_MATCHES_URL % (arbitroHref, currentYear, season)
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        laLigaHeadElement =  soup.find('div', class_='content-box-headline--logo')
        table = laLigaHeadElement.find_next_sibling()
        trs =  table.find_all('tr')
        trs = trs[2:]
        for tr in trs:
            tdsEquipos = tr.find_all('td', class_="no-border-links")
            equipo1TD = tdsEquipos[0]
            equipoName1 = equipo1TD.find('a').get('title', None) if equipo1TD.find('a') else None
            equipo2TD = tdsEquipos[1]
            equipoName2 = equipo2TD.find('a').get('title', None) if equipo2TD.find('a') else None
            resultadoTD = equipo2TD.find_next_sibling()
            resultado = resultadoTD.find('a', class_='ergebnis-link').text
            print(f"{equipoName1}\n{equipoName2}\n{resultado}")
    return

# referees = scrapeSeasonReferees(1, "2023")
# referees = referees + scrapeSeasonReferees(2, "2023")

# filename = "refs.json"
# with open(filename, 'w', encoding="utf-8") as json_file:
#     json.dump(referees, json_file, ensure_ascii=False)
filename = "refs.json"
with open(filename, 'r', encoding="utf-8") as json_file:
    referees = json.load(json_file)

referee = referees[0]
scrapeRefereeMatches(referee[0],referee[1])