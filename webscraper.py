import requests;
import pandas as pd;
import re;
import torch;
import math;
from datetime import date;
from collections import namedtuple;
from textblob import TextBlob;
from transformers import pipeline;
from bs4 import BeautifulSoup;

# load bert model and define helper task
sentiment_task = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest")

url = "https://www.nbcnews.com/us-news"
url2 = "https://abcnews.go.com/US"

agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

result = requests.get(url, headers=agent)
result2 = requests.get(url2, headers=agent)

nbcDoc = BeautifulSoup(result.text, "html.parser")
abcDoc = BeautifulSoup(result2.text, "html.parser")


article_titlesA = nbcDoc.find_all('h2', class_="styles_headline__ice3t") # NBC articles from lastest news, top stories, politics
article_titlesB = nbcDoc.find_all('h2', class_="wide-tease-item__headline") # NBC lower articles
article_titlesC = abcDoc.find_all('a', class_="AnchorLink News__Item external flex flex-row") # ABC articles

Article = namedtuple('Article', ['title', 'link', 'polarity'])
articlesAndLinks = [] # Stores articles and links as tuples
updatedArticlesAndLinks = []

# Webscraper stores articles and links as named tuples
for title in article_titlesA:
    if title.find('a'):
        tempArticle = Article(title=title.get_text(), link=title.find('a')['href'], polarity=0)
        articlesAndLinks.append(tempArticle)

for title in article_titlesB:
    if title.find('a'):

        tempArticle = Article(title=title.get_text(), link=title.find('a')['href'], polarity=0)
        articlesAndLinks.append(tempArticle)

for title in article_titlesC:
        
        tempArticle = Article(title=title.get_text(), link=title.get('href'), polarity=0)
        articlesAndLinks.append(tempArticle)

# text proprocessing using TextBlob
for article in articlesAndLinks:
    title, link, polarity = article

    # lowercase and remove punctuation, sentiment analysis with TextBlob
    textBlobTitle = title.lower()
    textBlobTitle = re.sub(r'[^\w\s]', '', str(title))

    blob = TextBlob(textBlobTitle)
    newPolarity = blob.sentiment.polarity

# sentiment analysis using BERT

    if sentiment_task(title)[0]['label'] == 'positive':
         polNum = 1
    elif sentiment_task(title)[0]['label'] == 'neutral':
         polNum = 0
    else:
        polNum = -1

    # gives a polarity rating based on sentiment label and score based of combined TextBlob and BERT scores
    newPolarity = round(((newPolarity + polNum*sentiment_task(title)[0]['score'])*10), 2)

    updatedArticle = Article(title, link, newPolarity)
    updatedArticlesAndLinks.append(updatedArticle)

df = pd.DataFrame(updatedArticlesAndLinks, columns = ['Title', 'Link', 'Polarity'])

today = date.today()
print('\n')
print("Today's date:", today)
print('Articles scraped: ', len(df)+1)
print('\n')

polarityMean = round(df[df['Polarity'] != 0]['Polarity'].mean(),2)
if polarityMean > 5:
     sentiment = 'Overwhelmingly Positive'
elif polarityMean > .5:
     sentiment = 'Mostly Positive'
elif polarityMean < .5:
     sentiment = "Mostly Negative"
elif polarityMean < 5:
     sentiment = "Overwhelmingly Negative"
else:
     sentiment = "Neutral"

print('Overall sentiment:', sentiment)
print('Sentiment score:', polarityMean)
positivityScore = round(df[df['Polarity'] > 0]['Polarity'].mean(), 2)
print('Positivity score:', positivityScore, 'out of 10')
negativityScore = round(df[df['Polarity'] < 0]['Polarity'].mean() * -1, 2)
print('Negativity score:', negativityScore, 'out of 10')

#testpush