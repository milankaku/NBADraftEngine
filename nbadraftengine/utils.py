from urllib.request import urlopen

import matplotlib.pyplot as ppt
import pandas
import seaborn
from bs4 import BeautifulSoup


def get_draft_data():
    """
    Return data frame of draft data from 1996-2016
    in proper format and save as CSV.

    :return: all_drafts: Pandas DataFrame
    """
    url_draft_years = "http://www.basketball-reference.com/draft/NBA_{year}.html"
    all_drafts = pandas.DataFrame()

    # combine draft data from 1996 to current to one data frame
    for year in range(1996, 2017):
        url = url_draft_years.format(year=year)

        html_from_url = urlopen(url)

        bs = BeautifulSoup(html_from_url, 'html.parser')

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


def create_yearly_draft_ws48_plot(data_frame):
    """
    Plot career average WS/48 by draft year

    :param data_frame: Pandas DataFrame
    """
    seaborn.set_style("white")
    ppt.figure(figsize=(13, 10))

    x_values = data_frame.Draft_Year.unique()
    y_values = data_frame.groupby('Draft_Year').WS_per_48.mean()
    ppt.title('Average Career Win Shares per 48 minutes by Draft Year (1996-2016)', fontsize=20)
    ppt.ylabel('Win Shares per 48 minutes', fontsize=18)
    ppt.xlim(1996, 2016)
    ppt.ylim(0, .10)
    ppt.grid(axis='y', color='grey', linestyle='--', lw=0.5, alpha=0.5)
    ppt.tick_params(axis='both', labelsize=14)

    seaborn.despine(left=True, bottom=True)

    ppt.plot(x_values, y_values)

    ppt.savefig('../graphs/ws_48_avg.png')


def create_round_based_ws48_plot(data_frame):
    """
    Plot career average WS/48 for first and second round picks
    by draft year

    :param data_frame: Pandas DataFrame
    """
    # plot WS/48 of first round and second round picks on same plot
    seaborn.set_style("white")
    seaborn.set_color_codes()

    first_round_picks = data_frame[data_frame['Rk'] < 31]
    first_round_ws48 = first_round_picks.groupby('Draft_Year').WS_per_48.mean()
    second_round_picks = data_frame[data_frame['Rk'] >= 31]
    second_round_ws48 = second_round_picks.groupby('Draft_Year').WS_per_48.mean()
    x_values = data_frame.Draft_Year.unique()
    fig, ax1 = ppt.subplots(figsize=(14, 11))
    ppt.title('Average Career Win Shares per 48 minutes for First Round and Second Round Draft Picks (1996-2016)',
              fontsize=20)
    ppt.grid(axis='y', color='grey', linestyle='--', lw=0.5, alpha=0.5)
    ppt.tick_params(axis='both', labelsize=15)

    plot1 = ax1.plot(x_values, first_round_ws48, 'b', label='First Round Picks Avg Career WS/48')
    ax1.set_ylabel('Win Shares per 48 minutes', fontsize=18)
    ax1.set_ylim(0, .11)

    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    # second Axes object for second round picks
    ax2 = ax1.twinx()
    plot2 = ax2.plot(x_values, second_round_ws48, 'r', label='Second Round Picks Avg Career WS/48')
    ax2.set_ylabel('Win Shares per 48 minutes', fontsize=18)
    ax2.set_ylim(0, .11)

    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    ax2.set_xlim(1996, 2017)

    lines = plot1 + plot2
    ax1.legend(lines, [l.get_label() for l in lines])
    for ax in [ax1, ax2]:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    ppt.savefig('../graphs/first_round_second_round_ws48_avg.png')


def create_each_pick_ws48_plot(data_frame):
    """
    Plot career average WS/48 by each draft pick
    :param data_frame: Pandas DataFrame
    """
    all_picks = data_frame[data_frame['Rk'] < 61]
    pick_avg_ws48 = all_picks.groupby('Rk').WS_per_48.mean()

    seaborn.set_style("white")
    ppt.figure(figsize=(13, 10))

    # create point plot
    ppt.figure(figsize=(9, 14))

    # plot point returns mean and confidence intervals at 95 CI by default
    ax = seaborn.pointplot(x='WS_per_48', y='Rk', join=False, data=all_picks, orient='h')

    title_per_pick_plot = ('Average Win Shares per 48 Minutes (with 95% CI)'
                           '\nfor each NBA Draft Pick in the Top 60 (1996-2016)')
    ax.set_title(title_per_pick_plot, fontsize=10, y=1.06)
    ax.set_ylabel('Draft Pick', fontsize=8, rotation=0)
    ax.set_xlabel('WS/48', fontsize=8)
    ax.tick_params(axis='both', labelsize=7)

    # pad for y axis so no overlap
    ax.yaxis.labelpad = 28

    ax.set_xlim(-0.1, 0.16)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    # add lines
    for y in range(len(pick_avg_ws48)):
        ax.hlines(y, -0.1, 0.16, color='grey', linestyle='--', lw=0.5)
    ax.vlines(0.00, -1, 60, color='grey', linestyle='--', lw=0.5)

    ppt.savefig('../graphs/ws48_avg_by_pick.png')
