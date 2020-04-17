import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from clean_data import *
from calculate_metrics import *

filepath_fights = './input/raw_total_fight_data.csv'
FIGHTS_RAW = pd.read_csv(filepath_fights, sep=';', index_col=False)

filepath_fighters = './input/raw_fighter_details.csv'
FIGHTERS = pd.read_csv(filepath_fighters, index_col='fighter_name')

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
FIGHTS = FIGHTS_RAW.copy()
ReplaceAccStat(FIGHTS, acc_cols)
ReplacePctStat(FIGHTS, pct_cols)
FIGHTS['weight_class'] = FIGHTS['Fight_type'].apply(GetWeightClass)
FIGHTS = CalcFightTime(FIGHTS)

# get the average of all statistics for every fighter, throughout their career
FIGHT_AVG = CalcAvgFight(FIGHTS, acc_cols)

# get a DataFrame with the fighter orig names, new names with weight class, and
# weight class
WEIGHT_CLASS = GetClassFromFighter(pd.DataFrame(FIGHT_AVG.index))

# calculate average for each accuracy column
WEIGHT_CLASS_AVG = CalcAvgPerClass(FIGHT_AVG, WEIGHT_CLASS, acc_cols)
WEIGHT_CLASS_AVG = WEIGHT_CLASS_AVG.reindex(weight_class_sort)

# get the total number of fights, per fighter
FIGHT_COUNT = CalcNumFights(FIGHTS)
