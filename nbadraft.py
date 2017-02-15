from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas

url = "http://www.basketball-reference.com/draft/NBA_2016.html"

html_from_url = urlopen(url)

bs = BeautifulSoup(html_from_url, 'html.parser')

table_row = bs.findAll('tr', limit=2)[1].findAll('th')

headers = [th.getText() for th in bs.findAll('tr', limit=2)[1].findAll('th')]

player_data_rows = bs.findAll('tr')[2:]

player_data = [[td.getText() for td in player_data_rows[i].findAll('td')]
               for i in range(len(player_data_rows))]

#Redundant data
headers.remove('Pk')

data_frame = pandas.DataFrame( player_data, columns=headers )

data_frame = data_frame[data_frame.Player.notnull()]

# Make header names more readable/clear
data_frame.rename(columns={'WS/48': 'WS per 48'}, inplace=True)
data_frame.columns = data_frame.columns.str.replace('%', '_PERC')
data_frame.columns.values[14:18] = [data_frame.columns.values[14:18][col] + " per Game" for col in range(4)]

print(data_frame.dtypes)