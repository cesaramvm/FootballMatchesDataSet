from datetime import datetime
import requests
from bs4 import BeautifulSoup

def scrapeSelectValues(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        select_element = soup.find('select', {'class': 'chzn-select'})
        if select_element:
            option_values = [option['value'] for option in select_element.find_all('option')]
            return option_values
    return None

def parseArrayFunc(date_strings):
    formatted_dates = [f'datetime.strptime("{date}", \'%Y-%m-%d\')' for date in date_strings]
    return ', '.join(formatted_dates)

# Call the function to scrape select values
select_values = scrapeSelectValues("https://www.transfermarkt.es/laliga-smartbank/marktwerteverein/wettbewerb/ES2/plus/")

formatted_dates = parseArrayFunc(select_values)
print(formatted_dates)