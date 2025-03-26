import requests
import datetime
import json
import html
from bs4 import BeautifulSoup


currentDate = "28.03.2025"#datetime.datetime.today().strftime('%d.%m.%Y')
url = "https://clickandplay.bg/тенис-клуб-каратанчева--reservation-" + currentDate + "-189.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
table = soup.find( 'table', attrs= { 'class': 'new-table-res day-graphic'} )
tableRows = table.find_all('tr')
eightHourRow = tableRows[2]
cells = eightHourRow.find_all('td')

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


print(availableCourts)
