from bs4 import BeautifulSoup
# import main
import sender
import hashlib
from datetime import datetime
import json


class Race:
    def __init__(self, race, age, candidates):
        # generate id hash from race
        # allows recieving server to check if they want to create or update
        self.id = hashlib.sha256(str.encode(race)).hexdigest()[0:18]
        self.race = race
        self.reporting = age
        self.candidates = candidates
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def json(self):
        return json.dumps(self.__dict__)
    
    
    

def scrape(html):

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
        sender.send(race.json())