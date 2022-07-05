#Autor original Ricardo Moya https://github.com/RicardoMoya/FootballMatchesDataSet

from FootballScraper import *
from FutbolClasses import *

LOAD_MARKET_VALUES()
startScrape(TEMPORADAS)
saveInfo('TestSave.txt')


#
# loadInfo('DataSetPartidos.1.txt')

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