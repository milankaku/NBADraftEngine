from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas

def get_draft_data():
    url_draft_years = "http://www.basketball-reference.com/draft/NBA_{year}.html"

    all_drafts = pandas.DataFrame()

    # combine draft data from 1996 to current to one data frame
    for year in range(1996, 2017):
        url = url_draft_years.format(year=year)

        html_from_url = urlopen(url)

        bs = BeautifulSoup(html_from_url, 'html.parser')

        table_row = bs.findAll('tr', limit=2)[1].findAll('th')

        headers = [th.getText() for th in bs.findAll('tr', limit=2)[1].findAll('th')]
        headers.remove('Pk')

        # player data starts after 2nd table record
        player_data_rows = bs.findAll('tr')[2:]

        player_data = [[td.getText() for td in player_data_rows[i].findAll('td')]
                       for i in range(len(player_data_rows))]

        year_data_frame = pandas.DataFrame(player_data, columns=headers)
        year_data_frame.insert(0, 'Draft_Year', year)

        all_drafts = all_drafts.append(year_data_frame, ignore_index=True)

    # Convert data to proper data types
    all_drafts = all_drafts.convert_objects(convert_numeric=True)

    # remove any rows that have null data
    all_drafts = all_drafts[all_drafts.Player.notnull()]

    # fill Not A Numbers to 0 and change some columns to int
    all_drafts = all_drafts[:].fillna(0)

    # Make header names more readable/clear
    all_drafts.rename(columns={'WS/48': 'WS_per_48'}, inplace=True)
    all_drafts.columns = all_drafts.columns.str.replace('%', '_PERC')

    all_drafts.columns.values[13:18] = [all_drafts.columns.values[13:18][col] + "_per_Game" for col in range(5)]

    all_drafts.loc[:, 'Yrs':'AST'] = all_drafts.loc[:, 'Yrs':'AST'].astype(int)

    # save data frame as a CSV
    all_drafts.to_csv("../csv/draft_data_1996_to_2016.csv")

    return all_drafts