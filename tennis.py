import json
import datetime
import html
import requests
from bs4 import BeautifulSoup
import argparse


DAY_RANGE = 7
TIME_OFFSET = 6

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
    targetRow = hour - TIME_OFFSET
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

def list_clubs():
    for key, value in tennisClubs.items():
        startIndex = value[0].find("bg")
        endIndex = value[0].find("r")
        clubName = value[0][startIndex+3:endIndex]
        print(f"Club name: { clubName.capitalize() } id: { key }")

def add_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("hour", help="Desired hour to get available courts for - 7..22", action="store_true" )
    parser.add_argument("court", help="Club from which to get available courts", action="store_true" )
    parser.add_argument("-l","--list", help="List available clubs", action="store_true" )
    return parser.parse_args()

if __name__ == "__main__":
    args = add_arguments()
    if args.list:
        list_clubs()
    else:
        print_available_courts( hour = 8 )
