from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas
import numpy as np

import matplotlib.pyplot as ppt
import seaborn

url_draft_years = "http://www.basketball-reference.com/draft/NBA_{year}.html"

all_drafts = pandas.DataFrame()

#combine draft data from 1996 to current to one data frame
for year in range(1996, 2017):
    url = url_draft_years.format(year=year)

    html_from_url = urlopen(url)

    bs = BeautifulSoup(html_from_url, 'html.parser')

    table_row = bs.findAll('tr', limit=2)[1].findAll('th')

    headers = [th.getText() for th in bs.findAll('tr', limit=2)[1].findAll('th')]
    headers.remove('Pk')

    #player data starts after 2nd table record
    player_data_rows = bs.findAll('tr')[2:]

    player_data = [[td.getText() for td in player_data_rows[i].findAll('td')]
                   for i in range(len(player_data_rows))]

    year_data_frame = pandas.DataFrame(player_data, columns=headers)
    year_data_frame.insert(0, 'Draft_Year', year)

    all_drafts = all_drafts.append(year_data_frame, ignore_index=True)

# Convert data to proper data types
all_drafts = all_drafts.convert_objects(convert_numeric=True)

#remove any rows that have null data
all_drafts = all_drafts[all_drafts.Player.notnull()]

#fill Not A Numbers to 0 and change some columns to int
all_drafts = all_drafts[:].fillna(0)

# Make header names more readable/clear
all_drafts.rename(columns={'WS/48': 'WS_per_48'}, inplace=True)
all_drafts.columns = all_drafts.columns.str.replace('%', '_PERC')

all_drafts.columns.values[13:18] = [all_drafts.columns.values[13:18][col] + "_per_Game" for col in range(5)]

all_drafts.loc[:,'Yrs':'AST'] = all_drafts.loc[:,'Yrs':'AST'].astype(int)

all_drafts.to_csv("draft_data_1996_to_2016.csv")

draft_df = pandas.read_csv("draft_data_1996_to_2016.csv", index_col=0)

WS48_yearly_avg = draft_df.groupby('Draft_Year').WS_per_48.mean()

#plot WS per 48 yearly averages
seaborn.set_style("white")
ppt.figure(figsize=(13,10))

x_values = draft_df.Draft_Year.unique()
y_values = WS48_yearly_avg
ppt.title('Average Career Win Shares per 48 minutes by Draft Year (1996-2016)', fontsize=20)
ppt.ylabel('Win Shares per 48 minutes', fontsize=18)
ppt.xlim(1996, 2016)
ppt.ylim(0, .10)
ppt.grid(axis='y', color='grey', linestyle='--', lw=0.5, alpha=0.5)
ppt.tick_params(axis='both', labelsize=14)

seaborn.despine(left=True, bottom=True)

ppt.plot(x_values, y_values)
ppt.show()
