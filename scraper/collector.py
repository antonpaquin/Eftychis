import twitter

ckey = 'ZECffFRPEMsaIjL4ChCm4G50i'
csecret = 'Ulc77A99RvZ1IPEWxeeR1QutgB6Ffft1qkg9LKPDBjrEh2aoiX'

api = twitter.Api(
    consumer_key=ckey,
    consumer_secret=csecret,
    application_only_auth=True,
    sleep_on_rate_limit=True
    )

def getTweets(geocode, max_id):
    return api.GetSearch(
        geocode=geocode,
        max_id=max_id,
        count=100,
        result_type='recent'
    )

def minId(li):
    return min([t.id for t in li])
