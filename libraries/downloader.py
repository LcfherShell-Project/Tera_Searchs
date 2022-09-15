import requests
from bs4 import BeautifulSoup

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
proxies = {"https": "http://223.241.0.250:3000", "http": "http://223.241.0.250:3000"}
htmldata = requests.session().get('https://www.xvideos.com/', proxies=proxies, headers=headers)
print(htmldata.text)