import json
import datetime
import html
import requests
from bs4 import BeautifulSoup

DAY_RANGE = 7
tennisClubs = {
    0 : ("https://clickandplay.bg/тенис-клуб-каратанчева--reservation-", "-189.html"),
    1 : ("https://clickandplay.bg/тк-1882--reservation-","-193.html"),
    2 : ("https://clickandplay.bg/360-тенис-клуб-бившият-бсфс--reservation-", "-100.html"),
    3 : ("https://clickandplay.bg/софия-тех-спорт-reservation-","-208.html")
}
def print_available_courts( hour ):
    currentDate = datetime.datetime.today()
    for day in range( 0, DAY_RANGE ):
        date = (currentDate + datetime.timedelta(days=day)).strftime('%d.%m.%Y')
        weekDay = datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%A')
        print(f"Geting Courts for { date } at { hour }:00 - { weekDay }" )
        url = tennisClubs[0][0] + date + tennisClubs[0][1]
        cells = get_hour_row(url, hour )
        courts = get_courts_from_table(cells)
        if( len(courts) > 0 ):
            for court in courts:
                courtNum = court[1]
                print(f"Court No. {courtNum} available ")
        else:
            print("No courts available!")

def get_hour_row( url, hour ):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find( 'table', attrs= { 'class': 'new-table-res day-graphic'} )
    tableRows = table.find_all('tr')
    targetRow = hour - 6
    wantedRow = tableRows[targetRow]
    return wantedRow.find_all('td')

def get_courts_from_table( cells ):
    availableCourts = []
    for cell in cells:
        for court in cell.find_all('div'):
            if court.has_attr('onclick'):
                startIndex = court['onclick'].index("{")
                endIndex = court['onclick'].rindex("}") + 1
                jsonString = court['onclick'][startIndex:endIndex]
                jsonString = html.unescape(jsonString)
                data = json.loads(jsonString)
                courtNumber = data['court'][0:1] if data['court'][0:1].isdigit() else data['court']
                availableCourts.append( ( data['date'], courtNumber , data['hour'] ) )

    return availableCourts


if __name__ == "__main__":
    hour = 8
    print_available_courts( hour )
