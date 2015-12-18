import pandas as pd
import tweepy
from datetime import datetime

consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def get_tweet_daterange(start_date,stop_date,screen_name):
	data = []
	tweets = api.user_timeline(screen_name=screen_name,count=200)
	while True:
		tweets_after_start = [tweet for tweet in tweets if tweet.created_at >= start_date]
		if len(tweets_after_start) == 0:
			break
		max_id = tweets_after_start[-1].id - 1
		data.extend(tweets_after_start)
		tweets = api.user_timeline(screen_name=screen_name,max_id=max_id,count=200)
	tweets = [[obj.user.screen_name.encode('utf-8'),obj.user.name.encode('utf-8'),obj.user.id,obj.user.description.encode('utf-8'),obj.created_at.year,obj.created_at.month,obj.created_at.day,"%s.%s"%(obj.created_at.hour,obj.created_at.minute),obj.id_str,obj.text.encode('utf-8')] for obj in data if obj.created_at <= stop_date ]
	dataframe=pd.DataFrame(tweets,columns=['screen_name','name','twitter_id','description','year','month','date','time','tweet_id','tweet'])
	dataframe.to_csv("%s_tweets.csv"%(screen_name),index=False)


if __name__ == '__main__':
	start_date  = datetime(2015,12,16)
	stop_date  = datetime(2015,12,18,10)
	screen_name = 'FinancialTimes'
	get_tweet_daterange(start_date,stop_date,screen_name)


