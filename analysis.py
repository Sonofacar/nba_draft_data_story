# Imports
import pandas as pd
import numpy as np
import dataframe_image as dfi
from plotnine import *

# Load data
path = 'homework/Stat_386/data-story/'
data = pd.read_csv(path + 'pick-data.csv')

# Definition of All-Star
# * 15+ pts per game
# * 30+ mins per game
# * 10+ vorp
def is_allstar(data):
    score = 0
    if (data.Points_pg > 20):
        score += 1
    if (data.Minutes_pg > 30):
        score += 1
    if (data.Value_over_replacement > 10):
        score += 1
    if (score == 3):
        return True
    else:
        return False

# Mutating the data
data_revised = data.loc[:, ['Pick', 'Minutes_pg', 'Points_pg', 'Value_over_replacement']]
data_revised['Is_allstar'] = data_revised.apply(is_allstar, axis = 1)

# Make a Custom Theme
def custom_theme():
    return (theme(panel_background = element_rect(fill = '#242629'),
                  plot_background = element_rect(fill = '#242629'),
                  legend_background = element_rect(fill = '#242629'),
                  legend_key = element_rect(fill = '#242629'),
                  text = element_text(color = 'white'),
                  axis_line = element_line(size = 0, color = '#242629'))) 

# Probability table of all-stars
stars = data.loc[data_revised.Is_allstar == True,:].groupby(pd.cut(data.Pick, np.arange(0,61,5))).count()['Unnamed: 0']
not_stars = data.loc[data_revised.Is_allstar == False,:].groupby(pd.cut(data.Pick, np.arange(0,61,5))).count()['Unnamed: 0']
prob = stars / (stars + not_stars)
table = pd.DataFrame(np.transpose([stars, not_stars, prob]))
table.columns = ['All-stars', 'Not All-stars', 'Proportion of All-stars Drafted']
table.Pick = ['1-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-55', '56-60']
dfi.export(table, path + 'table.png', table_conversion = 'selenium')

# Making a visualization
(ggplot(data_revised.loc[data_revised.Is_allstar, 'Pick'].reset_index()) +
 geom_density(aes(x = 'Pick'), color = '#F71480', fill = '#F71480', alpha = .4) +
 xlim((0,60)) +
 labs(title = 'Amount of NBA All-stars Drafted (2004-2018)',
      y = '',
      x = 'Pick') +
 custom_theme()).save(path + 'density.png')
