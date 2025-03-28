import json
import datetime
import html
import requests
from bs4 import BeautifulSoup

DAY_RANGE = 7

def print_available_courts():
    currentDate = datetime.datetime.today()
    allCourts = {}
    for day in range( 0, DAY_RANGE ):
        date = currentDate + datetime.timedelta(days=day)
        url = "https://clickandplay.bg/тенис-клуб-каратанчева--reservation-" + date.strftime('%d.%m.%Y') + "-189.html"
        cells = get_hour_row(url)
        allCourts += get_courts_from_table(cells)

    if allCourts.items() == 0:
        print(f'No available courts in the next {DAYS_RANGE} days')
    else:
        for court in allCourts:
            courtNum = court['court'][0:1]
            courtHour = court['hour']
            courtDate = court['date']
            print(f"Court No. {courtNum} available on { courtDate } at { courtHour } ")

def get_hour_row( url ):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find( 'table', attrs= { 'class': 'new-table-res day-graphic'} )
    tableRows = table.find_all('tr')
    wantedRow = tableRows[2]
    return wantedRow.find_all('td')

def get_courts_from_table( cells ):
    availableCourts = {}
    print("Geting Courts...")
    for cell in cells:
        for court in cell.find_all('div'):
            if court.has_attr('onclick'):
                startIndex = court['onclick'].index("{")
                endIndex = court['onclick'].rindex("}") + 1
                jsonString = court['onclick'][startIndex:endIndex]
                jsonString = html.unescape(jsonString)
                data = json.loads(jsonString)
                availableCourts[int(data['court'][0:1])] = [data['date'], data['hour']]

    return availableCourts


if __name__ == "__main__":
    print_available_courts()
