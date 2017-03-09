# NBADraftEngine

## What is it

**NBADraftEngine** is a  NBA Draft Application in development. It scrapes NBA draft and player
data from http://www.basketball-reference.com/ using BeautifulSoup. Different visualizations are created to interpret and analyze the data and player statistics.
Pandas, Matplotlib, and Seaborn libraries are utilized to visually represent this data.

First, I wanted to see the strength of draft classes over time by using Win Shares per 48 minutes (WS/48). This advanced statistic is a complex formula that is used to determine how much a player contributes to a team's win. I plotted the average WS/48 for all draft picks grouped by the year they were drafted (1996-2016).

![My image](https://github.com/milankaku/NBAStats/blob/master/graphs/ws_48_avg.png)


Next, I compared career WS/48 for first round picks to second round picks. In the NBA, almost all superstar and all-star caliber players are picked in the first round. In the NFL, it is not quite the same. The most talented are selected early, but teams often find great players in the deep rounds that go on to be Hall of Fame players. Obviously this is because there are more than 2 rounds unlike the NBA, but also the NBA is commonly reffered to as a "players league" and is star-driven. Every once in a while a 2nd round draft pick will emerge as a star, but it is not very common in the NBA. The data proved the fact that first round picks are likely going to have a better impact on a team's wins than a second round player. They are also more likely to have longer careers, so this can help their WS/48 stat.

![My image](https://github.com/milankaku/NBAStats/blob/master/graphs/first_round_second_round_ws48_avg.png)

I wanted to check the validity of the vastly held belief by NBA fans and pundits that the Association was "star-driven." To me, this means that the top picks in the NBA draft (who are most likely to be the stars and impact players as we saw above) were likely to have a higher career WS/48 average. This would be easier to see with a point plot with 95% Confidence Interval. This allows me to say I am 95% confident that the career WS/48 average for each draft pick falls between those 2 values. From the significant drop off in WS/48 after the 15th pick, it seems that the NBA is most likely star-driven and top heavy in terms of talent.

![My image](https://github.com/milankaku/NBAStats/blob/master/graphs/ws48_avg_by_pick.png)
