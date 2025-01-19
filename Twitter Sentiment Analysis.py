# Install required libraries
!pip install tweepy textblob matplotlib pandas

# Imports
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd

# Twitter API credentials (Replace with your own credentials)
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Function to fetch tweets
def fetch_tweets(query, count=100):
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en").items(count)
    tweet_list = [{"text": tweet.text, "created_at": tweet.created_at} for tweet in tweets]
    return pd.DataFrame(tweet_list)

# Function to analyze sentiment
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Input query and number of tweets
query = input("Enter the search query (e.g., 'Tesla'): ")
count = int(input("Enter the number of tweets to analyze: "))

# Fetch and analyze tweets
tweets_df = fetch_tweets(query, count)
tweets_df["Sentiment"] = tweets_df["text"].apply(analyze_sentiment)

# Display sentiment counts
sentiment_counts = tweets_df["Sentiment"].value_counts()
print("\nSentiment Counts:")
print(sentiment_counts)

# Visualize sentiment distribution
plt.figure(figsize=(8, 6))
sentiment_counts.plot(kind="bar", color=["green", "red", "blue"])
plt.title(f"Sentiment Analysis for '{query}'", fontsize=16)
plt.xlabel("Sentiment", fontsize=12)
plt.ylabel("Count", fontsize=12)
plt.xticks(rotation=0)
plt.show()
