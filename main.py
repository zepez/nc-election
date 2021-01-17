import asyncio
from pyppeteer import launch
import scraper
import os
import json

os.environ['pages'] = '["https://er.ncsbe.gov/?election_dt=11/03/2020&county_id=0&office=FED&contest=0", "https://er.ncsbe.gov/?election_dt=11/03/2020&county_id=0&office=CCL&contest=0"]'
os.environ['endpoint'] = 'http://localhost:3001/rail/test'
os.environ['cron'] = '* * * * *'
os.environ['headless'] = 'false'


async def main():
    #launch browser
    # checks env to know if headless
    # yes, true, t, 1 all eval to True. Otherwise false
    browser = await launch({"headless": os.environ.get('headless').lower() in ("yes", "true", "t", "1")})
    
    for page_to_scrape in json.loads(os.environ.get('pages')):
        # new page and go to location
        page = await browser.newPage()
        await page.goto(page_to_scrape)

        # get the entire page for parsing
        response = await page.evaluate('''() => {
            return document.documentElement.innerHTML
        }''')

        # call scrape data
        scraper.scrape(response)
        
    

	# close the broswer
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())

