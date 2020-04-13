import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from clean_data import *
from calculate_metrics import *

filepath_fights = './input/raw_total_fight_data.csv'
df_fights_raw = pd.read_csv(filepath_fights, sep=';', index_col=False)

filepath_fighters = './input/raw_fighter_details.csv'
df_fighters = pd.read_csv(filepath_fighters, index_col='fighter_name')

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
df_fights = get_fight_time(df_fights)

# get the average of all statistics for every fighter, throughout their career
fights_avg = calc_avg_fight(df_fights, acc_cols)

# get a DataFrame with the fighter orig names, new names with weight class, and
# weight class
weight_class = create_weight_class(pd.DataFrame(fights_avg.index))

# calculate average for each accuracy column
weight_class_avg = calc_avg_per_class(fights_avg, weight_class, acc_cols)
weight_class_avg = weight_class_avg.reindex(weight_class_sort)

# get the total number of fights, per fighter
fight_count = get_n_fights(df_fights)
