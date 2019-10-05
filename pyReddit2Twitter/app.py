import os
import praw
import requests
import time
import tweepy

# Chosen subreddits ("i.e. subreddit = "earthporn+winterporn")
subreddit = "<SUBREDDIT>"

def twitter_api():
    """
    Returns a Twitter API object with your Twitter API keys
    """
    auth = tweepy.OAuthHandler("<YOUR_CONSUMER_KEY>", "<YOUR_CONSUMER_SECRET>")
    auth.secure = True
    auth.set_access_token("<YOUR_ACCESS_TOKEN>","<YOUR_ACCESS_TOKEN_SECRET>")
    twitter_api = tweepy.API(auth)
    return twitter_api

def reddit_api():
    """
    Returns a Reddit API object with your Reddit API keys
    """
    reddit_api = praw.Reddit(client_id="<YOUR_CLIENT_ID>",
                            client_secret="<YOUR_CLIENT_SECRET>",
                            user_agent="<YOUR_USER_AGENT>")
    return reddit_api

def get_submissions_stream(subreddit):
    """
    Returns a subreddit submission stream
    """
    r = reddit_api()
    submissions_stream = r.subreddit(subreddit).stream.submissions()
    return submissions_stream

def tweet_image(twitter_api, url, message):
    """
    Downloads a file (mainly images) locally, posts it to your Twitter's timeline
    and then removes the file from the local repository. If the URL is not valid,
    (usually because of gifs or heavy files) then the URL itself is used as message
    """
    try:
        filename = 'temp.jpg'
        request = requests.get(url, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            twitter_api.update_with_media(filename, status=message)
            print(url + " uploaded successfully.")
            os.remove(filename)
        else:
            raise tweepy.TweepError([{'message': 'Error creating status.', 'code': 189}])
    except tweepy.TweepError as e:
        if e.api_code == 185:
            print("Rate limit exceeded. Please wait.")
            time.sleep(60*15)
        elif e.api_code == 189 or e.api_code == None:
            message += url
            twitter_api.update_status(message)
            print(url + " could not be directly uploaded. Permalink was used as message instead.")
        else:
            print(e)
            
def traverse_subreddit(submissions_stream):
    """
    Traverses subreddit's stream, posting a new status for each valid image.
    Reddit's title submission is used as the message for the status update
    """
    t = twitter_api()
    for media in submissions_stream:
        try:
            url = media.url
            message = media.title + " (at https://reddit.com" + media.permalink + ")"
            tweet_image(t, url, message)
        except tweepy.TweepError as e:
            if e.api_code == 187:
                print(url + " is a duplicate status. Skipping it.")
                continue
        finally:
            time.sleep(60)

traverse_subreddit(get_submissions_stream(subreddit))
