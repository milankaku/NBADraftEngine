from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas

url = "http://www.basketball-reference.com/draft/NBA_2016.html"

htmlFromUrl = urlopen(url)

bs = BeautifulSoup(htmlFromUrl, 'html.parser')
