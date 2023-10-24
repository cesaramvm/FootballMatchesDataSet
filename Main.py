#Autor original Ricardo Moya https://github.com/RicardoMoya/FootballMatchesDataSet

from DatosTemporada import *
import UtilsAndGlobals as ut
#from pretty_errors import activate
from icecream import install
from colorama import Fore, Back, Style
import MarketHelper as mh
install()
#activate()

def main(divisiones, temporadas, loadFromFile):
    for division in divisiones:
        print("****  PROCESANDO DIVISIÓN %s ****" % division)
        for temporada in temporadas:
            print("****  PROCESANDO TEMPORADA %s ****" % temporada)
            seasonData = DatosTemporada(division, temporada, loadFromFile)
            #seasonData.printSeasonResults()
            seasonData.printSeasonWinner()
            ut.ADD_SEASON_INFO(division, temporada, seasonData)
            ut.SAVE_MARKET_VALUES(ut.SAVE_MARKET_PATH)

loadFromFile = False
temporadas = ut.ALL_TEMPORADAS
divisiones = [2,1]
ut.LOAD_MARKET_VALUES(ut.SAVE_MARKET_PATH)
main(divisiones, temporadas, loadFromFile)
ut.SAVE_MARKET_VALUES(ut.SAVE_MARKET_PATH)
ut.SAVE_ALL_SEASONS(ut.SAVE_SEASONS_PATH)
mh.SAVE_NOT_CORRECTED_NAMES()
mh.SAVE_NOT_IN_MARKET_NAMES()