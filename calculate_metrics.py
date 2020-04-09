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
    
    df_agg = df_stat.groupby('weight_class').mean().round(2)
    
    return df_agg