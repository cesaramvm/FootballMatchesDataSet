#Autor original Ricardo Moya https://github.com/RicardoMoya/FootballMatchesDataSet
from datetime import datetime
# De la web: http://www.bdfutbol.com. Para el historico de partidos de futbol
URLS = {1:"http://www.bdfutbol.com/es/t/t%s.html", 2:"http://www.bdfutbol.com/es/t/t%s2a.html"}
TEMPORADAS = ["1970-71", "1971-72", "1972-73", "1973-74", "1974-75", "1975-76", "1976-77", "1977-78", "1978-79", "1979-80", "1980-81", "1981-82", "1982-83", "1983-84", "1984-85", "1985-86", "1986-87", "1987-88", "1988-89", "1989-90", "1990-91", "1991-92", "1992-93", "1993-94", "1994-95", "1995-96", "1996-97", "1997-98", "1998-99", "1999-00", "2000-01", "2001-02", "2002-03", "2003-04", "2004-05", "2005-06", "2006-07", "2007-08", "2008-09", "2009-10", "2010-11", "2011-12", "2012-13", "2013-14", "2014-15", "2015-16", "2016-17", "2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23"]
SHORT_TEMPORADAS = ["2010-11", "2011-12", "2012-13", "2013-14", "2014-15", "2015-16", "2016-17", "2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23"]
LAST_TEMPORADA = ["2022-23"]
TIED_TEMPORADAS = ["1970-71","1974-75","1978-79","1980-81","1983-84","1993-94","2004-05","2006-07","2020-21","2021-22"]
# Para usar en transfermarkt.es/
MARKET_URL = {1:"https://www.transfermarkt.es/laliga/marktwerteverein/wettbewerb/ES1/plus/?stichtag=%s", 2:"https://www.transfermarkt.es/laliga-smartbank/marktwerteverein/wettbewerb/ES2/plus/?stichtag=%s"}
FECHAS_VALORES = [datetime.strptime("2023-10-15", '%Y-%m-%d'), datetime.strptime("2023-10-01", '%Y-%m-%d'), datetime.strptime("2023-09-15", '%Y-%m-%d'), datetime.strptime("2023-09-01", '%Y-%m-%d'), datetime.strptime("2023-08-15", '%Y-%m-%d'), datetime.strptime("2023-08-01", '%Y-%m-%d'), datetime.strptime("2023-07-15", '%Y-%m-%d'), datetime.strptime("2023-07-01", '%Y-%m-%d'), datetime.strptime("2023-06-15", '%Y-%m-%d'), datetime.strptime("2023-06-01", '%Y-%m-%d'), datetime.strptime("2023-05-15", '%Y-%m-%d'), datetime.strptime("2023-05-01", '%Y-%m-%d'), datetime.strptime("2023-04-15", '%Y-%m-%d'), datetime.strptime("2023-04-01", '%Y-%m-%d'), datetime.strptime("2023-03-15", '%Y-%m-%d'), datetime.strptime("2023-03-01", '%Y-%m-%d'), datetime.strptime("2023-02-15", '%Y-%m-%d'), datetime.strptime("2023-02-01", '%Y-%m-%d'), datetime.strptime("2023-01-15", '%Y-%m-%d'), datetime.strptime("2023-01-01", '%Y-%m-%d'), datetime.strptime("2022-12-15", '%Y-%m-%d'), datetime.strptime("2022-12-01", '%Y-%m-%d'), datetime.strptime("2022-11-15", '%Y-%m-%d'), datetime.strptime("2022-11-01", '%Y-%m-%d'), datetime.strptime("2022-10-15", '%Y-%m-%d'), datetime.strptime("2022-10-01", '%Y-%m-%d'), datetime.strptime("2022-09-15", '%Y-%m-%d'), datetime.strptime("2022-09-01", '%Y-%m-%d'), datetime.strptime("2022-08-15", '%Y-%m-%d'), datetime.strptime("2022-08-01", '%Y-%m-%d'), datetime.strptime("2022-07-15", '%Y-%m-%d'), datetime.strptime("2022-07-01", '%Y-%m-%d'), datetime.strptime("2022-06-15", '%Y-%m-%d'), datetime.strptime("2022-06-01", '%Y-%m-%d'), datetime.strptime("2022-05-15", '%Y-%m-%d'), datetime.strptime("2022-05-01", '%Y-%m-%d'), datetime.strptime("2022-04-15", '%Y-%m-%d'), datetime.strptime("2022-04-01", '%Y-%m-%d'), datetime.strptime("2022-03-15", '%Y-%m-%d'), datetime.strptime("2022-03-01", '%Y-%m-%d'), datetime.strptime("2022-02-15", '%Y-%m-%d'), datetime.strptime("2022-02-01", '%Y-%m-%d'), datetime.strptime("2022-01-15", '%Y-%m-%d'), datetime.strptime("2022-01-01", '%Y-%m-%d'), datetime.strptime("2021-12-15", '%Y-%m-%d'), datetime.strptime("2021-12-01", '%Y-%m-%d'), datetime.strptime("2021-11-15", '%Y-%m-%d'), datetime.strptime("2021-11-01", '%Y-%m-%d'), datetime.strptime("2021-10-15", '%Y-%m-%d'), datetime.strptime("2021-10-01", '%Y-%m-%d'), datetime.strptime("2021-09-15", '%Y-%m-%d'), datetime.strptime("2021-09-01", '%Y-%m-%d'), datetime.strptime("2021-08-15", '%Y-%m-%d'), datetime.strptime("2021-08-01", '%Y-%m-%d'), datetime.strptime("2021-07-15", '%Y-%m-%d'), datetime.strptime("2021-07-01", '%Y-%m-%d'), datetime.strptime("2021-06-15", '%Y-%m-%d'), datetime.strptime("2021-06-01", '%Y-%m-%d'), datetime.strptime("2021-05-15", '%Y-%m-%d'), datetime.strptime("2021-05-01", '%Y-%m-%d'), datetime.strptime("2021-04-15", '%Y-%m-%d'), datetime.strptime("2021-04-01", '%Y-%m-%d'), datetime.strptime("2021-03-15", '%Y-%m-%d'), datetime.strptime("2021-03-01", '%Y-%m-%d'), datetime.strptime("2021-02-15", '%Y-%m-%d'), datetime.strptime("2021-02-01", '%Y-%m-%d'), datetime.strptime("2021-01-15", '%Y-%m-%d'), datetime.strptime("2021-01-01", '%Y-%m-%d'), datetime.strptime("2020-12-15", '%Y-%m-%d'), datetime.strptime("2020-12-01", '%Y-%m-%d'), datetime.strptime("2020-11-15", '%Y-%m-%d'), datetime.strptime("2020-11-01", '%Y-%m-%d'), datetime.strptime("2020-10-15", '%Y-%m-%d'), datetime.strptime("2020-10-01", '%Y-%m-%d'), datetime.strptime("2020-09-15", '%Y-%m-%d'), datetime.strptime("2020-09-01", '%Y-%m-%d'), datetime.strptime("2020-08-15", '%Y-%m-%d'), datetime.strptime("2020-08-01", '%Y-%m-%d'), datetime.strptime("2020-07-15", '%Y-%m-%d'), datetime.strptime("2020-07-01", '%Y-%m-%d'), datetime.strptime("2020-06-15", '%Y-%m-%d'), datetime.strptime("2020-06-01", '%Y-%m-%d'), datetime.strptime("2020-05-15", '%Y-%m-%d'), datetime.strptime("2020-05-01", '%Y-%m-%d'), datetime.strptime("2020-04-15", '%Y-%m-%d'), datetime.strptime("2020-04-01", '%Y-%m-%d'), datetime.strptime("2020-03-15", '%Y-%m-%d'), datetime.strptime("2020-03-01", '%Y-%m-%d'), datetime.strptime("2020-02-15", '%Y-%m-%d'), datetime.strptime("2020-02-01", '%Y-%m-%d'), datetime.strptime("2020-01-15", '%Y-%m-%d'), datetime.strptime("2020-01-01", '%Y-%m-%d'), datetime.strptime("2019-12-15", '%Y-%m-%d'), datetime.strptime("2019-12-01", '%Y-%m-%d'), datetime.strptime("2019-11-15", '%Y-%m-%d'), datetime.strptime("2019-11-01", '%Y-%m-%d'), datetime.strptime("2019-10-15", '%Y-%m-%d'), datetime.strptime("2019-10-01", '%Y-%m-%d'), datetime.strptime("2019-09-15", '%Y-%m-%d'), datetime.strptime("2019-09-01", '%Y-%m-%d'), datetime.strptime("2019-08-15", '%Y-%m-%d'), datetime.strptime("2019-08-01", '%Y-%m-%d'), datetime.strptime("2019-07-15", '%Y-%m-%d'), datetime.strptime("2019-07-01", '%Y-%m-%d'), datetime.strptime("2019-06-15", '%Y-%m-%d'), datetime.strptime("2019-06-01", '%Y-%m-%d'), datetime.strptime("2019-05-15", '%Y-%m-%d'), datetime.strptime("2019-05-01", '%Y-%m-%d'), datetime.strptime("2019-04-15", '%Y-%m-%d'), datetime.strptime("2019-04-01", '%Y-%m-%d'), datetime.strptime("2019-03-15", '%Y-%m-%d'), datetime.strptime("2019-03-01", '%Y-%m-%d'), datetime.strptime("2019-02-15", '%Y-%m-%d'), datetime.strptime("2019-02-01", '%Y-%m-%d'), datetime.strptime("2019-01-15", '%Y-%m-%d'), datetime.strptime("2019-01-01", '%Y-%m-%d'), datetime.strptime("2018-12-15", '%Y-%m-%d'), datetime.strptime("2018-12-01", '%Y-%m-%d'), datetime.strptime("2018-11-15", '%Y-%m-%d'), datetime.strptime("2018-11-01", '%Y-%m-%d'), datetime.strptime("2018-10-15", '%Y-%m-%d'), datetime.strptime("2018-10-01", '%Y-%m-%d'), datetime.strptime("2018-09-15", '%Y-%m-%d'), datetime.strptime("2018-09-01", '%Y-%m-%d'), datetime.strptime("2018-08-15", '%Y-%m-%d'), datetime.strptime("2018-08-01", '%Y-%m-%d'), datetime.strptime("2018-07-15", '%Y-%m-%d'), datetime.strptime("2018-07-01", '%Y-%m-%d'), datetime.strptime("2018-06-15", '%Y-%m-%d'), datetime.strptime("2018-06-01", '%Y-%m-%d'), datetime.strptime("2018-05-15", '%Y-%m-%d'), datetime.strptime("2018-05-01", '%Y-%m-%d'), datetime.strptime("2018-04-15", '%Y-%m-%d'), datetime.strptime("2018-04-01", '%Y-%m-%d'), datetime.strptime("2018-03-15", '%Y-%m-%d'), datetime.strptime("2018-03-01", '%Y-%m-%d'), datetime.strptime("2018-02-15", '%Y-%m-%d'), datetime.strptime("2018-02-01", '%Y-%m-%d'), datetime.strptime("2018-01-15", '%Y-%m-%d'), datetime.strptime("2018-01-01", '%Y-%m-%d'), datetime.strptime("2017-12-15", '%Y-%m-%d'), datetime.strptime("2017-12-01", '%Y-%m-%d'), datetime.strptime("2017-11-15", '%Y-%m-%d'), datetime.strptime("2017-11-01", '%Y-%m-%d'), datetime.strptime("2017-10-15", '%Y-%m-%d'), datetime.strptime("2017-10-01", '%Y-%m-%d'), datetime.strptime("2017-09-15", '%Y-%m-%d'), datetime.strptime("2017-09-01", '%Y-%m-%d'), datetime.strptime("2017-08-15", '%Y-%m-%d'), datetime.strptime("2017-08-01", '%Y-%m-%d'), datetime.strptime("2017-07-15", '%Y-%m-%d'), datetime.strptime("2017-07-01", '%Y-%m-%d'), datetime.strptime("2017-06-19", '%Y-%m-%d'), datetime.strptime("2017-06-15", '%Y-%m-%d'), datetime.strptime("2017-06-01", '%Y-%m-%d'), datetime.strptime("2017-05-15", '%Y-%m-%d'), datetime.strptime("2017-05-01", '%Y-%m-%d'), datetime.strptime("2017-04-15", '%Y-%m-%d'), datetime.strptime("2017-04-01", '%Y-%m-%d'), datetime.strptime("2017-03-15", '%Y-%m-%d'), datetime.strptime("2017-03-01", '%Y-%m-%d'), datetime.strptime("2017-02-15", '%Y-%m-%d'), datetime.strptime("2017-02-01", '%Y-%m-%d'), datetime.strptime("2017-01-15", '%Y-%m-%d'), datetime.strptime("2017-01-01", '%Y-%m-%d'), datetime.strptime("2016-12-15", '%Y-%m-%d'), datetime.strptime("2016-12-01", '%Y-%m-%d'), datetime.strptime("2016-11-15", '%Y-%m-%d'), datetime.strptime("2016-11-01", '%Y-%m-%d'), datetime.strptime("2016-10-15", '%Y-%m-%d'), datetime.strptime("2016-10-01", '%Y-%m-%d'), datetime.strptime("2016-09-15", '%Y-%m-%d'), datetime.strptime("2016-09-01", '%Y-%m-%d'), datetime.strptime("2016-08-15", '%Y-%m-%d'), datetime.strptime("2016-08-01", '%Y-%m-%d'), datetime.strptime("2016-07-15", '%Y-%m-%d'), datetime.strptime("2016-07-01", '%Y-%m-%d'), datetime.strptime("2016-06-15", '%Y-%m-%d'), datetime.strptime("2016-06-01", '%Y-%m-%d'), datetime.strptime("2016-05-15", '%Y-%m-%d'), datetime.strptime("2016-05-01", '%Y-%m-%d'), datetime.strptime("2016-04-15", '%Y-%m-%d'), datetime.strptime("2016-04-01", '%Y-%m-%d'), datetime.strptime("2016-03-15", '%Y-%m-%d'), datetime.strptime("2016-03-01", '%Y-%m-%d'), datetime.strptime("2016-02-15", '%Y-%m-%d'), datetime.strptime("2016-02-01", '%Y-%m-%d'), datetime.strptime("2016-01-15", '%Y-%m-%d'), datetime.strptime("2016-01-01", '%Y-%m-%d'), datetime.strptime("2015-12-15", '%Y-%m-%d'), datetime.strptime("2015-12-01", '%Y-%m-%d'), datetime.strptime("2015-11-15", '%Y-%m-%d'), datetime.strptime("2015-11-01", '%Y-%m-%d'), datetime.strptime("2015-10-15", '%Y-%m-%d'), datetime.strptime("2015-10-01", '%Y-%m-%d'), datetime.strptime("2015-09-15", '%Y-%m-%d'), datetime.strptime("2015-09-01", '%Y-%m-%d'), datetime.strptime("2015-08-15", '%Y-%m-%d'), datetime.strptime("2015-08-01", '%Y-%m-%d'), datetime.strptime("2015-07-15", '%Y-%m-%d'), datetime.strptime("2015-07-01", '%Y-%m-%d'), datetime.strptime("2015-06-15", '%Y-%m-%d'), datetime.strptime("2015-06-01", '%Y-%m-%d'), datetime.strptime("2015-05-15", '%Y-%m-%d'), datetime.strptime("2015-05-01", '%Y-%m-%d'), datetime.strptime("2015-04-15", '%Y-%m-%d'), datetime.strptime("2015-04-01", '%Y-%m-%d'), datetime.strptime("2015-03-15", '%Y-%m-%d'), datetime.strptime("2015-03-01", '%Y-%m-%d'), datetime.strptime("2015-02-15", '%Y-%m-%d'), datetime.strptime("2015-02-01", '%Y-%m-%d'), datetime.strptime("2015-01-15", '%Y-%m-%d'), datetime.strptime("2015-01-01", '%Y-%m-%d'), datetime.strptime("2014-12-15", '%Y-%m-%d'), datetime.strptime("2014-12-01", '%Y-%m-%d'), datetime.strptime("2014-11-15", '%Y-%m-%d'), datetime.strptime("2014-11-01", '%Y-%m-%d'), datetime.strptime("2014-10-23", '%Y-%m-%d'), datetime.strptime("2014-07-10", '%Y-%m-%d'), datetime.strptime("2014-05-15", '%Y-%m-%d'), datetime.strptime("2014-05-01", '%Y-%m-%d'), datetime.strptime("2014-04-15", '%Y-%m-%d'), datetime.strptime("2014-04-01", '%Y-%m-%d'), datetime.strptime("2014-03-15", '%Y-%m-%d'), datetime.strptime("2014-03-01", '%Y-%m-%d'), datetime.strptime("2014-02-15", '%Y-%m-%d'), datetime.strptime("2014-02-01", '%Y-%m-%d'), datetime.strptime("2014-01-15", '%Y-%m-%d'), datetime.strptime("2014-01-01", '%Y-%m-%d'), datetime.strptime("2013-12-15", '%Y-%m-%d'), datetime.strptime("2013-12-01", '%Y-%m-%d'), datetime.strptime("2013-11-15", '%Y-%m-%d'), datetime.strptime("2013-11-01", '%Y-%m-%d'), datetime.strptime("2013-10-15", '%Y-%m-%d'), datetime.strptime("2013-10-01", '%Y-%m-%d'), datetime.strptime("2013-09-15", '%Y-%m-%d'), datetime.strptime("2013-09-01", '%Y-%m-%d'), datetime.strptime("2013-08-15", '%Y-%m-%d'), datetime.strptime("2013-08-01", '%Y-%m-%d'), datetime.strptime("2013-07-15", '%Y-%m-%d'), datetime.strptime("2013-07-01", '%Y-%m-%d'), datetime.strptime("2013-06-15", '%Y-%m-%d'), datetime.strptime("2013-06-01", '%Y-%m-%d'), datetime.strptime("2013-05-15", '%Y-%m-%d'), datetime.strptime("2013-05-01", '%Y-%m-%d'), datetime.strptime("2013-04-15", '%Y-%m-%d'), datetime.strptime("2013-04-01", '%Y-%m-%d'), datetime.strptime("2013-03-15", '%Y-%m-%d'), datetime.strptime("2013-03-01", '%Y-%m-%d'), datetime.strptime("2013-02-15", '%Y-%m-%d'), datetime.strptime("2013-02-01", '%Y-%m-%d'), datetime.strptime("2013-01-15", '%Y-%m-%d'), datetime.strptime("2013-01-01", '%Y-%m-%d'), datetime.strptime("2012-12-15", '%Y-%m-%d'), datetime.strptime("2012-12-01", '%Y-%m-%d'), datetime.strptime("2012-11-15", '%Y-%m-%d'), datetime.strptime("2012-11-01", '%Y-%m-%d'), datetime.strptime("2012-10-15", '%Y-%m-%d'), datetime.strptime("2012-10-01", '%Y-%m-%d'), datetime.strptime("2012-09-15", '%Y-%m-%d'), datetime.strptime("2012-09-01", '%Y-%m-%d'), datetime.strptime("2012-08-15", '%Y-%m-%d'), datetime.strptime("2012-08-01", '%Y-%m-%d'), datetime.strptime("2012-07-15", '%Y-%m-%d'), datetime.strptime("2012-07-01", '%Y-%m-%d'), datetime.strptime("2012-06-15", '%Y-%m-%d'), datetime.strptime("2012-06-01", '%Y-%m-%d'), datetime.strptime("2012-05-15", '%Y-%m-%d'), datetime.strptime("2012-05-01", '%Y-%m-%d'), datetime.strptime("2012-04-15", '%Y-%m-%d'), datetime.strptime("2012-04-01", '%Y-%m-%d'), datetime.strptime("2012-03-15", '%Y-%m-%d'), datetime.strptime("2012-03-01", '%Y-%m-%d'), datetime.strptime("2012-02-15", '%Y-%m-%d'), datetime.strptime("2012-02-01", '%Y-%m-%d'), datetime.strptime("2012-01-15", '%Y-%m-%d'), datetime.strptime("2012-01-01", '%Y-%m-%d'), datetime.strptime("2011-12-15", '%Y-%m-%d'), datetime.strptime("2011-12-01", '%Y-%m-%d'), datetime.strptime("2011-11-15", '%Y-%m-%d'), datetime.strptime("2011-11-01", '%Y-%m-%d'), datetime.strptime("2011-10-15", '%Y-%m-%d'), datetime.strptime("2011-10-01", '%Y-%m-%d'), datetime.strptime("2011-09-15", '%Y-%m-%d'), datetime.strptime("2011-09-01", '%Y-%m-%d'), datetime.strptime("2011-08-15", '%Y-%m-%d'), datetime.strptime("2011-08-01", '%Y-%m-%d'), datetime.strptime("2011-07-15", '%Y-%m-%d'), datetime.strptime("2011-06-15", '%Y-%m-%d'), datetime.strptime("2011-06-01", '%Y-%m-%d'), datetime.strptime("2011-05-15", '%Y-%m-%d'), datetime.strptime("2011-05-01", '%Y-%m-%d'), datetime.strptime("2011-04-15", '%Y-%m-%d'), datetime.strptime("2011-04-01", '%Y-%m-%d'), datetime.strptime("2011-03-15", '%Y-%m-%d'), datetime.strptime("2011-03-01", '%Y-%m-%d'), datetime.strptime("2011-02-15", '%Y-%m-%d'), datetime.strptime("2011-02-01", '%Y-%m-%d'), datetime.strptime("2011-01-15", '%Y-%m-%d'), datetime.strptime("2011-01-01", '%Y-%m-%d'), datetime.strptime("2010-12-15", '%Y-%m-%d'), datetime.strptime("2010-12-01", '%Y-%m-%d'), datetime.strptime("2010-11-15", '%Y-%m-%d'), datetime.strptime("2010-11-01", '%Y-%m-%d')]
NAMES_CORRECTION = {'AD Almería': 'Almería', 'AD Ceuta': 'AD Ceuta', 'Alavés': 'Alavés', 'Albacete': 'Albacete', 'Alcorcón': 'Alcorcón', 'Alcoyano': 'Alcoyano', 'Algeciras': 'Algeciras', 'Alicante': 'Alicante', 'Almería': 'Almería', 'Alzira': 'Alzira', 'Amorebieta': 'Amorebieta', 'Andorra': 'Andorra', 'Athletic Club': 'Athletic Club', 'Athletic Club B': 'Athletic Club B', 'Atlético Madrileño': 'Atlético de Madrid B', 'Atlético Marbella': 'Atlético Marbella', 'Atlético de Bilbao': 'Athletic Club', 'Atlético de Madrid': 'Atlético de Madrid', 'Atlético de Madrid B': 'Atlético de Madrid B', 'Avilés Industrial': 'Avilés Industrial', 'Badajoz': 'Badajoz', 'Baracaldo': 'Baracaldo', 'Barcelona': 'Barcelona', 'Barcelona Atlético': 'Barcelona B', 'Barcelona B': 'Barcelona B', 'Betis': 'Betis', 'Bilbao Athletic': 'Athletic Club', 'Burgos': 'Burgos CF', 'Burgos CF': 'Burgos CF', 'CD Málaga': 'Málaga', 'Calvo Sotelo': 'Calvo Sotelo', 'Cartagena': 'FC Cartagena', 'Castellón': 'Castellón', 'Castilla': 'Real Madrid Castilla', 'Celta de Vigo': 'Celta de Vigo', 'Ciudad de Murcia': 'Ciudad de Murcia', 'Compostela': 'Compostela', 'Cultural Leonesa': 'Cultural Leonesa', 'Cádiz': 'Cádiz', 'Córdoba': 'Córdoba', 'Deportivo Aragón': 'Deportivo Aragón', 'Deportivo de La Coruña': 'Deportivo de La Coruña', 'Écija': 'Écija', 'Eibar': 'Eibar', 'Elche': 'Elche', 'Ensidesa': 'Ensidesa', 'Espanyol': 'Espanyol', 'Español': 'Espanyol', 'Extremadura': 'Extremadura', 'Extremadura UD': 'Extremadura UD', 'FC Cartagena': 'FC Cartagena', 'Ferrol': 'Racing de Ferrol', 'Figueres': 'Figueres', 'Fuenlabrada': 'Fuenlabrada', 'Getafe': 'Getafe', 'Getafe Deportivo': 'Getafe', 'Gijón': 'Sporting de Gijón', 'Gimnàstic de Tarragona': 'Gimnàstic de Tarragona', 'Gimnástico de Tarragona': 'Gimnàstic de Tarragona', 'Girona': 'Girona', 'Granada': 'Granada', 'Granada 74': 'Granada 74', 'Guadalajara': 'Guadalajara', 'Huesca': 'Huesca', 'Hércules': 'Hércules', 'Ibiza': 'Ibiza', 'Jaén': 'Jaén', 'Langreo': 'Langreo', 'Las Palmas': 'Las Palmas', 'Leganés': 'Leganés', 'Levante': 'Levante', 'Linares CF': 'Linares CF', 'Llagostera': 'Llagostera', 'Lleida': 'Lleida', 'Logroñés': 'UD Logroñés', 'Lorca': 'Lorca', 'Lorca Deportiva': 'Lorca Deportiva', 'Lorca FC': 'Lorca FC', 'Lugo': 'Lugo', 'Mallorca': 'Mallorca', 'Mallorca B': 'Mallorca B', 'Mestalla': 'Mestalla', 'Mirandés': 'Mirandés', 'Mollerussa': 'Mollerussa', 'Moscardó': 'Moscardó', 'Murcia': 'Murcia', 'Málaga': 'Málaga', 'Málaga B': 'Málaga B', 'Mérida': 'Mérida', 'Numancia': 'Numancia', 'Onteniente': 'Onteniente', 'Orense': 'Ourense', 'Orihuela': 'Orihuela', 'Osasuna': 'Osasuna', 'Ourense': 'Ourense', 'Oviedo': 'Oviedo', 'Palamós': 'Palamós', 'Palencia CF': 'Palencia CF', 'Polideportivo Ejido': 'Polideportivo Ejido', 'Ponferradina': 'Ponferradina', 'Pontevedra': 'Pontevedra', 'Racing de Ferrol': 'Racing de Ferrol', 'Racing de Santander': 'Racing de Santander', 'Rayo Majadahonda': 'Rayo Majadahonda', 'Rayo Vallecano': 'Rayo Vallecano', 'Real Burgos': 'Burgos CF', 'Real Madrid': 'Real Madrid', 'Real Madrid B': 'Real Madrid Castilla', 'Real Madrid Castilla': 'Real Madrid Castilla', 'Real Sociedad': 'Real Sociedad', 'Real Sociedad B': 'Real Sociedad B', 'Real Unión': 'Real Unión', 'Recreativo de Huelva': 'Recreativo de Huelva', 'Reus': 'Reus', 'Sabadell': 'Sabadell', 'Salamanca': 'Salamanca', 'San Andrés': 'San Andrés', 'Santander': 'Racing de Santander', 'Sestao': 'Sestao', 'Sevilla': 'Sevilla', 'Sevilla Atlético': 'Sevilla Atlético', 'Sporting de Gijón': 'Sporting de Gijón', 'Tarrasa': 'Tarrasa', 'Tenerife': 'Tenerife', 'Terrassa': 'Terrassa', 'Toledo': 'Toledo', 'UCAM Murcia': 'UCAM Murcia', 'UD Logroñés': 'UD Logroñés', 'Universidad de Las Palmas': 'Universidad de Las Palmas', 'Valencia': 'Valencia', 'Valladolid': 'Valladolid', 'Vecindario': 'Vecindario', 'Villarreal': 'Villarreal', 'Villarreal B': 'Villarreal B', 'Xerez': 'Xerez', 'Zaragoza': 'Zaragoza'}

MARKET_NAMES_CORRECTION = {'Alavés': 'Deportivo Alavés', 'Albacete': 'Albacete Balompié', 'Almería': 'UD Almería', 'Athletic Club': 'Athletic Club', 'Atlético de Madrid': 'Atlético de Madrid', 'Barcelona': 'FC Barcelona', 'Betis': 'Real Betis Balompié', 'Burgos CF': 'Burgos CF', 'CD Málaga': 'Málaga CF', 'Cartagena': 'FC Cartagena', 'Celta de Vigo': 'RC Celta de Vigo', 'Cádiz': 'Cádiz CF', 'Eibar': 'SD Eibar', 'Elche': 'Elche CF', 'Espanyol': 'RCD Espanyol', 'Getafe': 'Getafe CF', 'Girona': 'Girona FC', 'Granada': 'Granada CF', 'Huesca': 'SD Huesca', 'Ibiza': 'UD Ibiza', 'Las Palmas': 'UD Las Palmas', 'Leganés': 'CD Leganés', 'Levante': 'Levante UD', 'Lugo': 'CD Lugo', 'Mallorca': 'RCD Mallorca', 'Mirandés': 'CD Mirandés', 'Osasuna': 'CA Osasuna', 'Oviedo': 'Real Oviedo', 'Ponferradina': 'SD Ponferradina', 'Racing de Santander': 'Racing de Santander', 'Rayo Vallecano': 'Rayo Vallecano', 'Real Madrid': 'Real Madrid CF', 'Real Sociedad': 'Real Sociedad', 'Sevilla': 'Sevilla FC', 'Sporting de Gijón': ['Sporting de Gijón', 'Real Sporting de Gijón'], 'Tenerife': 'CD Tenerife', 'Valencia': 'Valencia CF', 'Valladolid': 'Real Valladolid CF', 'Villarreal': 'Villarreal CF', 'Villarreal B': 'Villarreal CF B', 'Zaragoza': 'Real Zaragoza'}

# sorted_dict = {k: v for k, v in sorted(MARKET_NAMES_CORRECTION.items())}
# print(str(sorted_dict))

TIED_SEASON_WINNERS = {
    1:{
        "1970-71":"Valencia",
        "1980-81":"Real Sociedad",
        "1983-84":"Athletic Club",
        "1993-94":"Barcelona",
        "2006-07":"Real Madrid"},
    2:{
        "1974-75":"Oviedo",
        "1978-79":"Almería",
        "1980-81":"Castellón",
        "1983-84":"Real Madrid Castilla",
        "2004-05":"Cádiz",
        "2020-21":"Espanyol",
        "2021-22":"Almería",}
}