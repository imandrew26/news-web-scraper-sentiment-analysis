from bs4 import BeautifulSoup;
import requests;
import pandas as pd;

url = "https://www.nbcnews.com/us-news"
url2 = "https://abcnews.go.com/US"

agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

result = requests.get(url, headers=agent)
result2 = requests.get(url2, headers=agent)

nbcDoc = BeautifulSoup(result.text, "html.parser")
abcDoc = BeautifulSoup(result2.text, "html.parser")

articlesAndLinks = [] # Stores articles and links as tuples

article_titlesA = nbcDoc.find_all('h2', class_="styles_headline__ice3t") # NBC articles from lastest news, top stories, politics
article_titlesB = nbcDoc.find_all('h2', class_="wide-tease-item__headline") # NBC filler articles

article_titlesC = abcDoc.find_all('a', class_="AnchorLink News__Item external flex flex-row")
print(len(article_titlesC))


for title in article_titlesA:
    if title.find('a'):
        title_text = title.get_text()
        link = title.find('a')['href']
        articlesAndLinks.append((title_text, link))

for title in article_titlesB:
    if title.find('a'):
        title_text = title.get_text()
        link = title.find('a')['href']
        articlesAndLinks.append((title_text, link))

for title in article_titlesC:
        title_text = title.get_text()
        link = title.get('href')
        articlesAndLinks.append((title_text, link))


df = pd.DataFrame(articlesAndLinks, columns = ['Title', 'Link'])
print(df)


#testpush