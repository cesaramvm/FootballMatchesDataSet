#Autor original Ricardo Moya https://github.com/RicardoMoya/FootballMatchesDataSet

from DatosTemporada import *
import UtilsAndGlobals as ut
from pretty_errors import activate
from icecream import install
install()

activate()

def main(divisiones, temporadas, loadFromFile):

    for division in divisiones:
        print("****  PROCESANDO DIVISIÓN %s ****" % division)
        for temporada in temporadas:
            if temporada == "2022-23":
                print("2022 2023 cuidadin")
            print("****  PROCESANDO TEMPORADA %s ****" % temporada)
            seasonData = DatosTemporada(division, temporada)
            if loadFromFile:
                seasonData.loadFromFile()
            else:
                seasonData.loadFromScraping()
            
            #seasonData.printSeasonResults()
            seasonData.printSeasonWinner()
            ut.ADD_SEASON_INFO(division, temporada, seasonData)


    ut.SAVE_ALL_SEASONS(ut.SAVE_FILE)
loadFromFile = True
temporadas = ut.ALL_TEMPORADAS
divisiones = [2,1]
ut.LOAD_MARKET_VALUES()
main(divisiones, temporadas, loadFromFile)
ut.SAVE_MARKET_VALUES()