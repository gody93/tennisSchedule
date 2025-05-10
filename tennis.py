import json
import datetime
import html
import requests
from bs4 import BeautifulSoup
import argparse


DAY_RANGE = 7

tennisClubs = {
    0 : ("https://clickandplay.bg/тенис-клуб-каратанчева--reservation-", "-189.html"),
    1 : ("https://clickandplay.bg/тк-1882--reservation-","-193.html"),
    2 : ("https://clickandplay.bg/360-тенис-клуб-бившият-бсфс--reservation-", "-100.html"),
    3 : ("https://clickandplay.bg/софия-тех-спорт-reservation-","-208.html"),
    4 : ("https://clickandplay.bg/15-40-reservation-","-5.html"),
    5 : ("https://clickandplay.bg/бароккоспорт-reservation-", "-15.html"),
    6 : ("https://clickandplay.bg/тк-хепи-уин-1-славия--reservation-", "-142.html"),
    7 : ("https://clickandplay.bg/тк-хепи-уин-2-славия-балон-❗%EF%B8%8F-reservation-", "-201.html")
}
def print_available_courts( hour, clubId ):
    currentDate = datetime.datetime.today()
    for day in range( 0, DAY_RANGE ):
        date = (currentDate + datetime.timedelta(days=day)).strftime('%d.%m.%Y')
        weekDay = datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%A')
        url = tennisClubs[clubId][0] + date + tennisClubs[clubId][1]
        cells = get_hour_row(url, hour )
        if cells == None:
            print("Club doesnt work in given hour!")
            return

        courts = get_courts_from_table(cells)
        if( len(courts) > 0 ):
            for court in courts:
                courtNum = court[1]
                if( args.hour ):
                    print(f"Court No. {courtNum} available for { date } at { hour:02d}:00 - { weekDay } ")
            print("---------------------")

def get_hour_row( url, hour ):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find( 'table', attrs= { 'class': 'new-table-res day-graphic'} )
    tableRows = table.find_all('tr')
    for hourRow in tableRows[1:]:
        timeStamp = hourRow.find('th', attrs = {'class': 'headcol td-hours'}).find('div').get('rel')
        timeStr = f"{hour:02d}:00"
        if timeStr == timeStamp:
            return hourRow.find_all('td')

    return None

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
        print(f"ID: { key }, { clubName.title().replace('-',' ') } ")

def add_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("hour", type=int, nargs="?", help="Desired hour to get available courts for - 7..22", default=8)
    parser.add_argument("id", type=int, nargs="?", help="Club from which to get available courts", default=0)
    parser.add_argument("-l","--list", help="List available clubs", action="store_true" )
    return parser.parse_args()

def extract_club_name( clubId ):
    startIndex = tennisClubs[clubId][0].find("bg")
    endIndex = tennisClubs[clubId][0].find("r")
    clubName = tennisClubs[clubId][0][startIndex+3:endIndex]
    return clubName.title().replace('-',' ')

if __name__ == "__main__":
    args = add_arguments()
    if args.list:
        list_clubs()
    else:
        hour = args.hour
        clubId = args.id
        print(extract_club_name(clubId))
        print_available_courts( hour, clubId )
