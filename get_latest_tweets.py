import pandas as pd
import tweepy

#Twitter API credentials

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def get_latest_tweets(screen_name):
	count=0
	latest_tweets=[]
	data=pd.read_csv("%s_tweets.csv"%(screen_name))
	since_Id=data['tweet_id'].loc[0]
	#print since_Id
	#try:
	#	tweet=api.get_status(since_Id).text
	#except tweepy.error.TweepError:
	#	print "No tweet found on id %s.\nCode Terminated\n"%(since_id)
	#	exit()
	try:
		new_tweets=api.user_timeline(screen_name=screen_name,since_id=since_Id,count=200)
		old = new_tweets[-1].id - 1
	except IndexError:
		print "No new tweets"
		exit()
	count=len(new_tweets)
	print "%s tweets downloaded so far"%(count)
	latest_tweets.extend(new_tweets)
	print latest_tweets[0].id
	while len(new_tweets) <= 200:
		#print "getting latest tweets\n"
		new_tweets=api.user_timeline(screen_name=screen_name,max_id=old,since_id=since_Id,count=200)
		count = count + len(new_tweets)
		print "in loop %s tweets downloaded so far"%(len(new_tweets))
		#print new_tweets[0].id
		latest_tweets.extend(new_tweets)
		old=latest_tweets[-1].id - 1
		#print old,since_Id,len(new_tweets)
        print count
	new_data=[[obj.user.screen_name,obj.user.name,obj.user.id_str,obj.user.description.encode("utf8"),obj.created_at.year,obj.created_at.month,obj.created_at.day,"%s.%s"%(obj.created_at.hour,obj.created_at.minute),obj.id_str,obj.text.encode("utf8")] for obj in latest_tweets ]
	dataframe=pd.DataFrame(new_data,columns=['screen_name','name','twitter_id','description','year','month','date','time','tweet_id','tweet'])
	dataframe=[dataframe,data]
	dataframe=pd.concat(dataframe)
	dataframe.to_csv("%s_tweets.csv"%(screen_name),index=False)

if __name__=='__main__':
	get_latest_tweets("TimesNow")
