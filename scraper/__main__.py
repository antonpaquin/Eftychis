import time
import threading

import collector
import store

from geocodes import geocodes

'''
We're going to grab a set of tweets from each geocode, and stash the minimum
id (oldest) within each set.

From there, we grab a new set of tweets corresponding to the geocode with the
maximum min_id (newest) among the sets.

The idea is, by doing this we'll grab tweets over a roughly equal timespan for
each geocode. This weights things by population / tweet density about how we
like it.
'''

min_ids = []

for geocode in geocodes:
    # This starts us out at whenever we started the scraper
    li = collector.getTweets(geocode, None)
    # Stash them in ES
    store.putMany(li, geocode)
    # And remember the minimum ID of this set
    min_ids.append(collector.minId(li))

def searchMax():
    global ratelimit, numScraped

    # Get the targt as described above
    target = min_ids.index(max(min_ids))

    # Run a search on that target
    li = collector.getTweets(geocodes[target], min_ids[target])

    # Update the min_id for this geocode

    # And put them in ES
    store.putMany(li, geocodes[target])

    # Maintain a count of how far we've come
    numScraped += len(li)

    # And how fast we can go
    ratelimit += 1

# track how many tweets we've scraped
numScraped = 0
scrapeLimit = 2000000

# Twitter limits us to 450 calls in a 15 minute period
ratelimit = 0
ratelimitMax = 435 # Be a bit safe

# We'll start a thread here to allow rate limit things to happen
def ratelimitDecrement():
    global ratelimit

    # If we don't go faster than this, we won't hit the limit
    interval = (15 * 60) / (450)
    while(True):
        if ratelimit > 0:
            ratelimit -= 1
        time.sleep(interval)

t = threading.Thread(target=ratelimitDecrement)
t.start()

# use some file IO to keep track of things in progress
logIncrement = 10000
logThreshold = logIncrement
def doLogging():
    with open('log.txt', 'a') as log_f:
        log_f.write('Scraped: {} \n'.format(str(numScraped)))
        log_f.write('Err: {} \n'.format(str(store.exceptionCount)))
        log_f.write('\n')

# And finally, run the scraper
while numScraped < scrapeLimit:
    if ratelimit < ratelimitMax:
        searchMax()
    else:
        time.sleep(2)
    if numScraped > logThreshold:
        logThreshold += logIncrement
        doLogging()
