'''
Created on Nov 20, 2018

@author: Deep
'''
from django.shortcuts import render
from django.http.response import JsonResponse
import tweepy
from textblob import TextBlob
import re, csv, itertools
import json, jsonpickle


def welcomePage(request):
    return render(request, "./homePage.html")


def sigmaTest(request):
    return render(request, "./SigmaTest.html")


def searchPage(request):
    return render(request, "./searchPage.html")


def resultPage(request):
    
    queryPara = request.POST['param']
    api = connect()
    
    tweets = fetch_tweets(api, query=queryPara, count=200)
    
    if len(tweets) > 0:
        
        #setEdges(tweets)
        # picking positive tweets from tweets 
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
#         plist = [tweet['display'] for tweet in ptweets]
        
        # percentage of positive tweets 
        posTweetPercentage = 100 * len(ptweets) / len(tweets)
        print("Positive tweets percentage: {} %".format(posTweetPercentage)) 
        # picking negative tweets from tweets 
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
        # percentage of negative tweets 
        negTweetPercentage = 100 * len(ntweets) / len(tweets)
        print("Negative tweets percentage: {} %".format(negTweetPercentage)) 
        # percentage of neutral tweets
        nuTweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
        nuTweetPercentage = 100 * len(nuTweets) / len(tweets)
        print("Neutral tweets percentage: {} %".format(nuTweetPercentage))
        jsonData = {"positive": posTweetPercentage, "negative": negTweetPercentage, "neutral":nuTweetPercentage}
        return JsonResponse(jsonData)
    else:
        jsonData = {"positive": 0, "negative": 0, "neutral":0}
        return JsonResponse(jsonData)


def fetch_tweets(api, query, count):
    maxTweets = count  # Some arbitrary large number
    tweetsPerQry = 100  # this is the max the API permits
    fName = 'Tweetment/tweets.txt'  # We'll store the tweets in a text file.
    
    sinceId = None
    
    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1000
    
    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    with open(fName, 'w') as f:
        while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = api.search(q=query + ' -filter:retweets', count=tweetsPerQry, lang='en', tweet_mode='extended')
                    else:
                        new_tweets = api.search(q=query + ' -filter:retweets', count=tweetsPerQry, lang='en', tweet_mode='extended',
                                                since_id=sinceId)
                else:
                    if (not sinceId):
                        new_tweets = api.search(q=query + ' -filter:retweets', count=tweetsPerQry, lang='en', tweet_mode='extended',
                                                max_id=str(max_id - 1))
                    else:
                        new_tweets = api.search(q=query + ' -filter:retweets', count=tweetsPerQry, lang='en', tweet_mode='extended',
                                                max_id=str(max_id - 1),
                                                since_id=sinceId)
                if not new_tweets:
                    print("No more tweets found")
                    break
                for tweet in new_tweets:
                    f.write(jsonpickle.encode(tweet._json, unpicklable=False) + 
                            '\n')
                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
            # Just exit if any error
                print("some error : " + str(e))
                break

    print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
    tweets = []
    with open(fName, 'r') as f:
        for line in f:
            parsed_tweet = {}
            data = json.loads(line)
            parsed_tweet['text'] = data['full_text']
            parsed_tweet['sentiment'] = get_tweet_sentiment(data['full_text'])
            parsed_tweet['display'] = data['user']['screen_name']
            hashTags = data['entities']['hashtags']
            tags = []
            if len(hashTags) != 0:
                for i in hashTags:
                    tags.append(i['text']);
            parsed_tweet['hashTags'] = tags
            if tweet.retweet_count > 0: 
                # if tweet has retweets, ensure that it is appended only once 
                if parsed_tweet not in tweets: 
                    tweets.append(parsed_tweet) 
            else: 
                tweets.append(parsed_tweet)
    print(tweets.__len__())
    return tweets


def connect():
    consumer_key = 'FWBcYLHlbW4YShHzOPTgyJgcO'
    consumer_secret = 'sH9JnCB3kwnYALLAxJh0lvE2nOZPH0h13Z2YI8oNZQ9jSp3E90'
    try: 
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api   
    except: 
        print("Error: Authentication Failed")

        
def clean_tweet(tweet):
    ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
    '''
    tweet = re.sub(r'\$\w*', '', tweet)
    tweet = re.sub('@[^\s]+', '', tweet)
    tweet = re.sub(r'\b\w{1,2}\b', '', tweet)  # use stop words
    tweet = re.sub(r'^RT[\s]+', '', tweet)
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
        
        # removing the hash # sign from the word
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub(r'^@[\s]', '', tweet)
    # print("clean - " + tweet)
    # case: empty tweets after cleasn, Questions sentence
    return tweet


def get_tweet_sentiment(tweet): 
    
    analysis = TextBlob(clean_tweet(tweet))  # self.clean_tweet(tweet)
    
    # set sentiment 
#     if(analysis.detect_language() != 'en'):
#         analysis = analysis.translate(to='en')
         
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else: 
        return 'negative'
    
    
def setEdges(tweets):
    print("Inside")
    with open('Tweetment/persons.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
        for i in range(len(tweets)):
            for j in range(i + 1, len(tweets)):
                a = tweets[i]['hashTags']
                b = tweets[j]['hashTags']
    #             print(a + b)
                if(len(a) > 0 and len(b) > 0):
                    if(len(set(a).intersection(b)) > 0):
                        filewriter.writerow([tweets[i]['display'],tweets[j]['display']])
                        #print (tweets[i]['display'] + " " + tweets[j]['display'])
    
