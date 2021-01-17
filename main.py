import asyncio
from pyppeteer import launch
import scraper
import os
import json

os.environ['pages'] = '["https://er.ncsbe.gov/?election_dt=11/03/2020&county_id=0&office=FED&contest=0", "https://er.ncsbe.gov/?election_dt=11/03/2020&county_id=0&office=CCL&contest=0"]'
os.environ['endpoint'] = ''
os.environ['cron'] = '* * * * *'


async def main():
    #launch browser
    browser = await launch({"headless": False})
    
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

