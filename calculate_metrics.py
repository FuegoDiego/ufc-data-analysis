import pandas as pd
import numpy as np
import pdb

from utils import *

def calc_avg_per_class(df, cols):
    # function to calculate the average statistic per weight class, e.g.
    # average significant strikes landed and attempted per weight class
    #
    # stat_col: column type to calculate average over, e.g. 'SIG_STR.'
    
    df = df.set_index('weight_class')
    
    df_stat = calc_fight_sums(df, cols)
    
    df_agg = df_stat.groupby('weight_class').mean().round(2)
    
    return df_agg

def calc_agg(df, cols):
    # function to calculate the sum and count of fight statistics, per corner
    #
    # df: DataFrame, contains fight data
    
    red_corner, blue_corner = get_corner_cols(df)
    
    df_red = df[red_corner].set_index('R_fighter')
    df_blue = df[blue_corner].set_index('B_fighter')
    
    df_red.index.names = ['fighter']
    df_blue.index.names = ['fighter']
    
    df_red_sum = df_red.groupby('fighter').sum()
    df_red_count = df_red.groupby('fighter').count()
    df_blue_sum = df_blue.groupby('fighter').sum()
    df_blue_count = df_blue.groupby('fighter').count()
    
    df_fighters_sum = df_red_sum.merge(df_blue_sum, on='fighter')
    df_fighters_count = df_red_count.merge(df_blue_count, on='fighter')
    
    df_fighters_sum = calc_fight_sums(df_fighters_sum, cols)
    df_fighters_count = calc_fight_sums(df_fighters_count, cols)
    
    cols_avg = list(map(lambda s: 'AVG_' + s, df_fighters_sum.columns))
    
    df_fighters = pd.DataFrame(df_fighters_sum.values / df_fighters_count.values
                               ,index=df_fighters_sum.index
                               ,columns=cols_avg)
    
    return df_fighters

# TODO: move to utils as a function that calculates the sum of red and blue
# corner statistics
def calc_fight_sums(df, cols):
    # function to get the total number of strikes, submissions, takedowns, etc.
    # in a fight
    #
    # df: DataFrame, contains fight data
    # cols: list(str), list of column names to calculate totals for
    
    # columns for landed and attempted
    red, blue = name_corner(cols)
    total_l, total_a = name_lnd_att(cols)
    red_l, red_a = name_lnd_att(red)
    blue_l, blue_a = name_lnd_att(blue)
    
    # columns to retrieve, and do calculations on
    cols_red = red_l + red_a
    cols_blue = blue_l + blue_a
    cols_total = total_l + total_a
    
    df_stat = pd.DataFrame(df[cols_red].values + df[cols_blue].values, index=df.index,
                      columns=cols_total)
    
    return df_stat
