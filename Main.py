#Autor original Ricardo Moya https://github.com/RicardoMoya/FootballMatchesDataSet

import UtilsAndGlobals as ut
from DatosTemporada import DatosTemporada

#from pretty_errors import activate
from icecream import install
from colorama import Fore, Back, Style
import MarketHelper as mh
install()
#activate()

def main():
    ut.loadFromFile = True
    ut.loadMarket = True
    ut.loadReferees = True
    ut.loadFromFile = not ut.loadFromFile
    ut.loadMarket = not ut.loadMarket
    ut.loadReferees = not ut.loadReferees

    temporadas = ut.SHORT_TEMPORADAS
    divisiones = [2,1]
    for division in divisiones:
        print("****  PROCESANDO DIVISIÓN %s ****" % division)
        for temporada in temporadas:
            print("****  PROCESANDO TEMPORADA %s ****" % temporada)
            seasonData = DatosTemporada(division, temporada)
            #seasonData.printSeasonResults()
            seasonData.printSeasonWinner()
            ut.ADD_SEASON_INFO(division, temporada, seasonData)        
            ut.SAVENOTTRANSFER()
            ut.SAVE_REFEREES_VALUES(ut.SAVE_REFEREES_PATH)

    ut.SAVE_REFEREES_VALUES(ut.SAVE_REFEREES_PATH)
    ut.SAVE_MARKET_VALUES(ut.SAVE_MARKET_PATH)
    ut.SAVE_ALL_SEASONS(ut.SAVE_SEASONS_PATH)


main()

