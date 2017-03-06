# NBAStats

## What is it

**NBAStats** is a   NBA Stats Application in development. It scrapes NBA player
and team data from http://www.basketball-reference.com/ using Python.
Pandas, Matplotlib, and Seaborn libraries are used to visually represent this data.

First, I plotted Win Shares per 48 minutes for all draft picks grouped by the year they were drafted (1996-2016).

![My image](https://github.com/milankaku/NBAStats/blob/master/ws_48_avg.png)


In the NBA, almost all superstar and all-star caliber players are picked in the first round. In the NFL, it is not quite the same. The most talented are selected early, but teams often find great players in the deep rounds that go on to be Hall of Fame players. Obviously this is because there are more than 2 rounds unlike the NBA, but also the NBA is commonly reffered to as a "players league" and is star-driven. Every once in a while a 2nd round draft pick will emerge as a star, but it is not very common in the NBA. I decided to compare career WS/48 for first round picks to second round picks. The data proved the fact that first round picks are likely going to have a better impact on a team's wins than a second round player. They are also more likely to have longer careers, so this can help their WS/48 stat.

![My image](https://github.com/milankaku/NBAStats/blob/master/first_round_second_round_ws48_avg.png)
