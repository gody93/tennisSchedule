import requests
import datetime
import json
import html
from bs4 import BeautifulSoup


def print_available_courts():

    currentDate = "28.03.2025"#datetime.datetime.today().strftime('%d.%m.%Y')
    url = "https://clickandplay.bg/тенис-клуб-каратанчева--reservation-" + currentDate + "-189.html"
    cells = get_hour_row(url)

    print(get_courts_from_table(cells))

def get_hour_row( url ):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find( 'table', attrs= { 'class': 'new-table-res day-graphic'} )
    tableRows = table.find_all('tr')
    wantedRow = tableRows[2]
    return wantedRow.find_all('td')

def get_courts_from_table( cells ):
    availableCourts = {}
    for cell in cells:
        for court in cell.find_all('div'):
            if court.has_attr('onclick'):
                startIndex = court['onclick'].index("{")
                endIndex = court['onclick'].rindex("}") + 1
                jsonString = court['onclick'][startIndex:endIndex]
                jsonString = html.unescape(jsonString)
                data = json.loads(jsonString)
                availableCourts[int(data['court'][0:1])] = [ data['date'], data['hour']]

    return availableCourts


if __name__ == "__main__":
    print_available_courts()
