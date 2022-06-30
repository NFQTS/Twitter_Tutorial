import tweepy # useful library for doing things with the twitter api. I just this for any data I need to POST to the API or to do things like change my banner/profile.
import requests # good for GET calls to the api to just get basic information
from keys import keys # allows us to keep our api keys stored outside of the this main script in a dictionary, for security purposes.

# These variables just get the API keys from the keys.py file, so if we share this script we don't give away our private keys
client_id = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']
bearer_token = keys['bearer_token']

# This is just giving the api info about our keys, we can ignore this basically. I honestly dont even understand these lol.
# FYI... To make a bot post to twitter you will need to apply for elevated access. I believe just a bearer token is required to scan for data, but the rest are for posting tweets etc...
headers = {"Authorization": "Bearer {}".format(bearer_token)}
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Now we can start doing stuff.


def scan_for_tweets_mentioning_rootroop():
    """ Scans the Twitter API for a list of tweets from the last 7 days that mentioned @RooTroopNFT."""
    url = "https://api.twitter.com/2/tweets/search/recent?query=%40RooTroopNFT&tweet.fields=author_id" #this is an "endpoint", which gives the Twitter API some information about what data to send us. Everything the API needs (besides authentication) is in this query.
    # to search for specific keywords, just use the API explorer and let it swap in/out the keywords for you until you understand how to change the endpoint yourself.

    response = requests.request("GET", url, headers=headers) # this sends the API call out, provides our authentication info to Twitter, and stores the response in a variable for us to work with.
    res_json = response.json() # this converts the response to JSON because supposedly it makes it easier to tell what's going on and work with... idk :P This is a LIST of information that we requested
    print(res_json)
    if res_json['meta']['result_count'] > 0: # checks that there are any results
        # IMPORTANT:
        # 'id' = the ID of the tweet (this comes with the tweet information by default), 'author_id = the ID of the person who tweeted (I had to add this in to the query when I specified the endpoint earlier)
        # That's why it says '.fields=author-id' at the end of the endpoint url
        # There are ways to also get their Twitter handle, i.e. @nf_qts... but it makes it more complicated (adds more code, and handles can change... IDs dont) you can always do that later as long as you have their author_id
        for tweet in res_json['data']: # cycles through each tweet and prints out the tweet data in your console to make it easier to understand what's going on
            print(tweet)


def scan_for_number_of_tweets_mentioning_rootroop():
    """ Scans the Twitter API for the number of times @RooTroopNFT was mentioned recently."""
    url = "https://api.twitter.com/2/tweets/counts/recent?query=%40RooTroopNFT" # our endpoint is slightly different this time. Notice it points to tweets/counts/recent instead of tweets/search/recent
    # url = "https://api.twitter.com/2/tweets/counts/recent?query=%40RooTroopNFT&granularity=day" # same endpoint as above, but shows the results per day instead of per hour
    response = requests.request("GET", url, headers=headers)  # same stuff as before
    res_json = response.json()  # same stuff as before

    # this response doesn't really need to check if there are results because if there were no mentions of @RooTroopNFT in a given hour... it'll just tell us 0
    # you can check for different timeframes, like days instead of hours, by changing your endpoint and adding the 'granularity' parameter. You can do this with the API exporer OR by changing the endpoint yourself
    # here's the endpoint for granularity changed to days, for an example
    # url = "https://api.twitter.com/2/tweets/counts/recent?query=%40RooTroopNFT&granularity=day"
    # I included that above and commented it out so you can toy with it :P

    for hour in res_json['data']: # loop that takes each result from the response and makes it easier to read in your console
        print(hour) # prints stuffz


def make_bot_tweet_something():
    """ Tells the API what we want to tweet and posts it."""
    status_update = "#RootyRoo baby LFG!" # text you would like to tweet out
    api.update_status(status=status_update) # tells Tweepy to create a tweet with that text
    # WARNING: Be careful not to spam with this. It won't even let you tweet the same thing twice in a row I don't think.
    # You can find ways to have it change what it says pretty easily to work around it not letting you post duplicate tweets, but DEFINITELY be careful of looping this.
    # Sending media (pics/gifs etc) is a pain if you don't have room to just post the url... since it requires you to upload the media and do wierd stuff. IDK how to do it well yet.


def make_bot_reply_to_tweet(tweet_id):
    """ Replies to a specific tweet"""
    stat_update = "Oh shit! I also like to #RootyRoo :D"
    api.update_status(status=stat_update, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True) # same thing as tweeting but requires the ID of the tweet to reply to.
    # For some reason replying to a tweet also requires that 'auto_populate_reply_metadata=True' parameter. Otherwise it just creates a regular tweet.
    # To automatically get the tweet ID, you would be using the previous queries for recent tweets, saving their tweet ID in some sort of list, and then giving this function that ID.


scan_for_tweets_mentioning_rootroop() # runs the function that scans to find tweets mentioning @RooTroopNFT
scan_for_number_of_tweets_mentioning_rootroop() # runs the function that scans to see how many times @RooTroopNFT was mentioned recently
make_bot_tweet_something()
make_bot_reply_to_tweet('1542640435792707584') # makes the bot reply to the tweet that I tell it to reply to. The number is the ID number of the tweet, which can be found via the API OR from the url of the tweet in the browser.
