#Autor original Ricardo Moya https://github.com/RicardoMoya/FootballMatchesDataSet

from DatosTemporada import *
import UtilsAndGlobals as ut
from pretty_errors import activate
from icecream import install
from colorama import Fore, Back, Style
install()
activate()



def main(divisiones, temporadas, loadFromFile):
    for division in divisiones:
        print("****  PROCESANDO DIVISIÓN %s ****" % division)
        for temporada in temporadas:
            if temporada == "2022-23":
                print(Fore.RED + "****  2022 2023 cuidadin ****"+Fore.RESET)
            print("****  PROCESANDO TEMPORADA %s ****" % temporada)
            seasonData = DatosTemporada(division, temporada)
            seasonData.loadFromFile() if loadFromFile else seasonData.loadFromScraping()
            #seasonData.printSeasonResults()
            seasonData.printSeasonWinner()
            ut.ADD_SEASON_INFO(division, temporada, seasonData)
    ut.SAVE_ALL_SEASONS(ut.SAVE_SEASONS_PATH)

loadFromFile = False
temporadas = ut.LAST_TEMPORADA
divisiones = [2,1]
ut.LOAD_MARKET_VALUES()
main(divisiones, temporadas, loadFromFile)
ut.SAVE_MARKET_VALUES()