import requests;
import pandas as pd;
import re;
import nltk;
from collections import namedtuple;
from textblob import TextBlob;
from transformers import BertTokenizer, BertModel
from bs4 import BeautifulSoup;


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
article_titlesB = nbcDoc.find_all('h2', class_="wide-tease-item__headline") # NBC filler articles

article_titlesC = abcDoc.find_all('a', class_="AnchorLink News__Item external flex flex-row")

Article = namedtuple('Article', ['title', 'preprocessedTitle', 'link', 'polarity'])
articlesAndLinks = [] # Stores articles and links as tuples
updatedArticlesAndLinks = []

for title in article_titlesA:
    if title.find('a'):
        tempArticle = Article(title=title.get_text(), preprocessedTitle=title.get_text(), link=title.find('a')['href'], polarity=0)
        articlesAndLinks.append(tempArticle)

for title in article_titlesB:
    if title.find('a'):

        tempArticle = Article(title=title.get_text(), preprocessedTitle=title.get_text(), link=title.find('a')['href'], polarity=0)
        articlesAndLinks.append(tempArticle)

for title in article_titlesC:
        
        tempArticle = Article(title=title.get_text(), preprocessedTitle=title.get_text(), link=title.get('href'), polarity=0)
        articlesAndLinks.append(tempArticle)

# text proprocessing using TextBlob
for article in articlesAndLinks:
    title, preprocessedTitle, link, polarity = article

    # lowercase and remove punctuation
    preprocessedTitle = preprocessedTitle.lower()
    preprocessedTitle = re.sub(r'[^\w\s]', '', str(preprocessedTitle))

    blob = TextBlob(preprocessedTitle)
    newPolarity = blob.sentiment.polarity

    updatedArticle = Article(title, preprocessedTitle, link, newPolarity)
    updatedArticlesAndLinks.append(updatedArticle)



df = pd.DataFrame(updatedArticlesAndLinks, columns = ['Title', 'Preprocessed Title', 'Link', 'Polarity'])
print(df)



#testpush