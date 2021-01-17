import asyncio
from pyppeteer import launch
import scraper



async def main():
    #launch browser
    browser = await launch({"headless": True})
    # new page and go to location
    page = await browser.newPage()
    await page.goto('https://er.ncsbe.gov/?election_dt=11/03/2020&county_id=0&office=FED&contest=0')

	# get the entire page for parsing
    response = await page.evaluate('''() => {
        return document.documentElement.innerHTML
    }''')

	# call scrape data
    scraper.scrape(response)

	# close the broswer
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())

