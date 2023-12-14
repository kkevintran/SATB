from textblob import TextBlob
from config import NEWS_API_KEY
import requests

def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def get_latest_news():
    news_url = "https://newsapi.org/v2/everything"
    params = {
        'apiKey': NEWS_API_KEY,
        'pageSize' : 50, # This means more bias towards recent news articles the lower the number of articles,
        'q': 'Nvidia',
        'language': 'en',
        'sortBy': 'PublishedAt'
    }

    response = requests.get(news_url, params=params)
    # print(response)
    news_data = response.json()
    # Returns an array of articles 
    return(news_data['articles'])

get_latest_news()

