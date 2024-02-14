from bs4 import BeautifulSoup;
import requests;
import pandas as pd;

url = "https://www.nbcnews.com/us-news"

agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

result = requests.get(url, headers=agent)

nbcDoc = BeautifulSoup(result.text, "html.parser")

articlesAndLinks = [] # Stores articles and links as tuples

article_titlesA = nbcDoc.find_all('h2', class_="styles_headline__ice3t") # Articles from lastest news, top stories, politics
article_titlesB = nbcDoc.find_all('h2', class_="wide-tease-item__headline") # Filler articles

for title in article_titlesA:
    title_text = title.get_text()
    link = title.find('a')['href']
    articlesAndLinks.append((title_text, link))

for title in article_titlesB:
    if title.find('a') is not None:
        title_text = title.get_text()
        link = title.find('a')['href']
        articlesAndLinks.append((title_text, link))

df = pd.DataFrame(articlesAndLinks, columns = ['Title', 'Link'])
print(df)

#testpush