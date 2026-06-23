# pyReddit2Twitter
A Twitter bot written in Python 3 who uploads images from a specific subreddit to your Twitter account

## Optional Xquik backend

The default backend remains Tweepy. To post through Xquik instead, set:

```env
POST_BACKEND=xquik
XQUIK_API_KEY=
XQUIK_ACCOUNT=
XQUIK_BASE_URL=https://xquik.com
```

When Xquik is enabled, Reddit image URLs are sent as public media URLs instead of being downloaded locally first.
