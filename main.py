import pandas as pd
import seaborn as sns

from clean_data import *

filepath_fights = './input/raw_total_fight_data.csv'
df_fights_raw = pd.read_csv(filepath_fights, sep=';', index_col=False)

#filepath_fighters = './input/raw_fighter_details.csv'
#df_fighters = pd.read_csv(filepath_fighters, index_col='fighter_name')

# set of type of columns that contains an accuracy stat, e.g. '15 of 24'
acc_cols = {'BODY', 'CLINCH', 'DISTANCE', 'GROUND', 'HEAD', 'LEG', 'SIG_STR.', 'TD', 'TOTAL_STR.'}

# set of columns that are perecentages
pct_cols = {'SIG_STR_pct', 'TD_pct'}

# copy the raw data and clean it
df_fights = df_fights_raw.copy()
replace_acc_stat(df_fights, acc_cols)
replace_pct_stat(df_fights, pct_cols)
df_fights['weight_class'] = df_fights['Fight_type'].apply(get_weight_class)
