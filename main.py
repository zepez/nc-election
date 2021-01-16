import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import json
import requests
from datetime import datetime



class Race:
    def __init__(self, race, age, candidates):
        self.id = race
        self.race = race
        self.reporting = age
        self.candidates = candidates
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def json(self):
        return json.dumps(self.__dict__)
    

def send_data(race):
    print(race.json())
    x = requests.post("http://localhost:3001/rail/test", data = race.json(), headers = {'Content-Type': 'application/json', 'Accept-Encoding': 'UTF-8'})
    print(x.status_code)


def scrape_data(html):

    soup = BeautifulSoup(html, 'html.parser')
    # need to map over all of these
    tables = soup.find_all("table", class_="grid_table") or []

    # loop over all tables
    for table in tables:
        # get the name of the race
        race = table.find('a').get_text()
        # get the amount of precincts reporting
        reporting = table.find_all('b')
        # only wan the third b tag
        reporting = reporting[2].get_text()
        
        # get all table rows
        rows = table.find_all('tr')
        # remove first two rows 
        rows.pop(0)
        rows.pop(0)
        
        candidates = []
        
        #loop through rows 
        for row in rows:
            cells = row.find_all("td")
            candidate = {}
            candidate["name"] = cells[0].get_text()
            candidate["party"] = cells[1].get_text()
            candidate["ballot_count"] = cells[2].get_text()
            candidate["percent"] = cells[3].get_text()
            candidates.append(candidate)
            

        race = Race(race, reporting, candidates)
        send_data(race)



async def main():
    #launch browser
    browser = await launch({"headless": True})
    # new page and go to location
    page = await browser.newPage()
    await page.goto('https://er.ncsbe.gov/?election_dt=11/03/2020&county_id=0&office=FED&contest=0')
    # take a screenshot (probably remove)
    await page.screenshot({'path': 'example.png'})

	# get the entire page for parsing
    response = await page.evaluate('''() => {
        return document.documentElement.innerHTML
    }''')

	# call scrape data
    scrape_data(response)

	# close the broswer
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())

