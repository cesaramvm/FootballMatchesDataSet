#Autor original Ricardo Moya https://github.com/RicardoMoya/FootballMatchesDataSet

import FootballScraper as fs
from DatosTemporada import *
import UtilsAndGlobals as ut



def main():

    for division in divisiones:
        print("****  PROCESANDO DIVISIÓN %s ****" % division)
        for temporada in temporadas:
            print("****  PROCESANDO TEMPORADA %s ****" % temporada)
            seasonData = DatosTemporada(division, temporada)
            if division in ut.ALL_SEASONS_INFO and temporada in ut.ALL_SEASONS_INFO[division]:
                print("FROM DATA")
                seasonData.loadFromData()
            else:
                print("FROM PARSE")
                seasonData.loadFromScraping()
            
            #seasonData.printSeasonResults()
            seasonData.printSeasonWinner()
            ut.ADD_SEASON_INFO(division, temporada, seasonData)


    ut.SAVE_ALL_SEASONS('TestSave.csv')

temporadas = ut.LAST_TEMPORADA
divisiones = [2,1]

ut.LOAD_MARKET_VALUES()
ut.LOAD_ALL_SEASONS('TestSave.csv')

#main()

#
# LOAD_ALL_SEASONS('DataSetPartidos.1.txt')

#
# from ScrapBDFutbol import *
# # Obtengo los partidos de futbol de las temporadas anteriores
# partidos = getInfo()
# fichero = open('DataSetPartidos.all.txt', 'w')
# fichero.write('idPartido::temporada::division::jornada::EquipoLocal::'
#               'EquipoVisitante::golesLocal::golesVisitante::fecha::timestamp\n')
# for value in partidos.values():
#     fichero.write('%s\n' % str(value))
#
# fichero.close()