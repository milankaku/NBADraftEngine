from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas


draft_year = int(input("Please enter a NBA draft year: "))

url = "http://www.basketball-reference.com/draft/NBA_%d.html" % draft_year

# draft_year = 2016
# url = "http://www.basketball-reference.com/draft/NBA_.html"

html_from_url = urlopen(url)

bs = BeautifulSoup(html_from_url, 'html.parser')

table_row = bs.findAll('tr', limit=2)[1].findAll('th')

headers = [th.getText() for th in bs.findAll('tr', limit=2)[1].findAll('th')]

#player data starts after 2nd table record
player_data_rows = bs.findAll('tr')[2:]

player_data = [[td.getText() for td in player_data_rows[i].findAll('td')]
               for i in range(len(player_data_rows))]

#Redundant data
headers.remove('Pk')

data_frame = pandas.DataFrame( player_data, columns=headers )

#remove any rows that have null data
data_frame = data_frame[data_frame.Player.notnull()]

# Make header names more readable/clear
data_frame.rename(columns={'WS/48': 'WS per 48'}, inplace=True)
data_frame.columns = data_frame.columns.str.replace('%', '_PERC')

data_frame.columns.values[13:18] = [data_frame.columns.values[13:18][col] + " per Game" for col in range(5)]

data_frame = data_frame.convert_objects(convert_numeric=True)

#fill Not A Numbers to 0 and change some columns to int
data_frame = data_frame[:].fillna(0)
data_frame.loc[:,'Yrs':'AST'] = data_frame.loc[:, 'Yrs':'AST'].astype(int)

data_frame.insert(1, 'Draft Year', draft_year)

print(data_frame.head())