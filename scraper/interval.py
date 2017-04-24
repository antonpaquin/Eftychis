import time
import threading

import collector
import store

from geocodes import geocodes

def fullcodes():
    global numScraped

    for geocode in geocodes:
        # This starts us out at whenever we started the scraper
        li = collector.getTweets(geocode, None)
        # Stash them in ES
        store.putMany(li, geocode)
        # Track number we got
        numScraped += len(li)

# track how many tweets we've scraped
numScraped = 0
scrapeLimit = 2000000

# use some file IO to keep track of things in progress
def doLogging():
    with open('log.txt', 'a') as log_f:
        log_f.write('Scraped: {} \n'.format(str(numScraped)))
        log_f.write('Err: {} \n'.format(str(store.exceptionCount)))
        log_f.write('\n')

# use async / threading to do our timing
scrape_interval_minutes = 60
def waitInterval():
    time.sleep(scrape_interval_minutes * 60)

# And finally, run the scraper
while True:
    t1 = threading.Thread(target=waitInterval)
    t2 = threading.Thread(target=fullcodes)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    doLogging()
