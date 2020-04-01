import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from clean_data import *
from calculate_metrics import *

filepath_fights = './input/raw_total_fight_data.csv'
df_fights_raw = pd.read_csv(filepath_fights, sep=';', index_col=False)

#filepath_fighters = './input/raw_fighter_details.csv'
#df_fighters = pd.read_csv(filepath_fighters, index_col='fighter_name')

# list of weight classes ordered from lowest weight to largest weight, with
# women divisions first. Catch, Open, and undefined weights go last
weight_class_sort = ["Women's Strawweight", "Women's Flyweight", 
                     "Women's Bantamweight", "Women's Featherweight",
                     'Flyweight', 'Bantamweight', 'Featherweight',
                     'Lightweight', 'Welterweight', 'Middleweight',
                     'Light Heavyweight', 'Heavyweight', 'Catchweight',
                     'Openweight', 'NA']

# set of type of columns that contains an accuracy stat, e.g. '15 of 24'
acc_cols = {'BODY', 'CLINCH', 'DISTANCE', 'GROUND', 'HEAD', 'LEG', 'SIG_STR.', 'TD', 'TOTAL_STR.'}

# set of columns that are perecentages
pct_cols = {'SIG_STR_pct', 'TD_pct'}

# copy the raw data and clean it
df_fights = df_fights_raw.copy()
replace_acc_stat(df_fights, acc_cols)
replace_pct_stat(df_fights, pct_cols)
df_fights['weight_class'] = df_fights['Fight_type'].apply(get_weight_class)


# TODO: re-label the columns in the plot so they are easier to read
# TODO: be able to plot heatmap for strikes landed or attempted only
df_avg = calc_avg_per_class(df_fights, acc_cols)
df_avg = df_avg.reindex(weight_class_sort)
df_avg = df_avg.drop(['Catchweight', 'Openweight', 'NA'])

sns.set(rc={'figure.figsize':(18,14)})

sns_plot = sns.heatmap(data=df_avg, annot=True, fmt='g')
plt.yticks(rotation=0)

fig = sns_plot.get_figure()
fig.savefig('strikes-per-wc.pdf')
