import pandas as pd
import numpy as np
import ipdb

def calc_avg_per_class(df, stat_col):
    # function to calculate the average statistic per weight class, e.g.
    # average significant strikes landed and attempted per weight class
    #
    # stat_col: column type to calculate average over, e.g. 'SIG_STR.'
    
    # columns for landed and attempted
    red_l = 'R_' + stat_col + '_L'
    red_a = 'R_' + stat_col + '_A'
    blue_l = 'B_' + stat_col + '_L'
    blue_a = 'B_' + stat_col + '_A'
    
    # columns to retrieve
    cols = ['weight_class', red_l, red_a, blue_l, blue_a]
    
    # copy dataframe to include only weight class, and the desired columns
    df_stat = df[cols].copy()
    
    # we want the sum of red and blue corner to get the total over the weight
    # class
    total_l = 'TOTAL_' + stat_col + 'L'
    total_a = 'TOTAL_' + stat_col + 'A'
    df_stat[total_l] = df_stat[red_l] + df_stat[blue_l]
    df_stat[total_a] = df_stat[red_a] + df_stat[blue_a]
    
    df_avg = df_stat.groupby('weight_class').mean()
    
    return df_stat