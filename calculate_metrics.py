import pandas as pd
import numpy as np
import pdb

from utils import *

def calc_avg_fight(df, cols):
    # function to calculate the averages per 15 minutes, per fighter
    #
    # df: DataFrame, contains fight data
    
    col_dict = read_col_map()['weight class']    
    
    red_corner_cols, blue_corner = get_corner_cols(df)
    
    # we want to append the total time of the fight in seconds in order to
    # calculate the average per 15 minutes
    red_corner_cols.extend(['total_time', 'weight_class'])
    blue_corner.extend(['total_time', 'weight_class'])
    
    red_corner = df[red_corner_cols]
    blue_corner = df[blue_corner]
    
    red_corner = red_corner.rename(columns={'R_fighter':'fighter'})
    blue_corner = blue_corner.rename(columns={'B_fighter':'fighter'})
    
    # we have to create new fighters for those who fight at multiple weight
    # classes, e.g. Jorge Masvidal fights and Lightweight and Welterweight
    # this way, the averages only count towards the weight class that the
    # fight happened at
    red_corner = create_by_wc(red_corner, col_dict)
    blue_corner = create_by_wc(blue_corner, col_dict)

    red_corner_sum = red_corner.groupby('fighter').sum()
    blue_corner_sum = blue_corner.groupby('fighter').sum()
    
    fights_sum = red_corner_sum.merge(blue_corner_sum, on='fighter', how='outer')
    fights_sum = fights_sum.fillna(0)

    fight_time = fights_sum['total_time_x'] + fights_sum['total_time_y']
    fight_time = fight_time.reset_index(name='total_time')
    fight_time = fight_time.set_index('fighter')

    fights_sum = calc_fight_sums(fights_sum, cols)
    
    cols_avg = list(map(lambda s: s + '_p15', fights_sum.columns))
    cols_sum = fights_sum.loc[:, fights_sum.columns != 'total_time'].columns.values
    
    cols_rename = {cols_sum[i]: cols_avg[i] for i in range(len(cols_sum))}

    fights_sum = fights_sum.join(fight_time, on='fighter')
    
    fights_avg = fights_sum.div(fights_sum['total_time'] / 60 / 15, axis=0)
    
    del fights_avg['total_time']
    
    fights_avg = fights_avg.rename(columns=cols_rename)
    
    return fights_avg

def calc_avg_per_class(fights_avg, weight_class, cols):
    # function to calculate the average statistic per weight class, e.g.
    # average significant strikes landed and attempted per weight class
    #
    # stat_col: column type to calculate average over, e.g. 'SIG_STR.'

    fights_avg = fights_avg.merge(weight_class[['fighter', 'weight_class']], on='fighter')

    weight_class_avg = fights_avg.groupby('weight_class').mean().round(2)
    
    return weight_class_avg

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

def get_n_fights(df):
    # function to get a DataFrame containing the number of fights per fighter
    #
    # df: DataFrame, contains fight data
    
    fighter_counts = df[['R_fighter', 'B_fighter']]

    red_counts = fighter_counts.groupby('R_fighter').size().reset_index(name='R_counts')
    blue_counts = fighter_counts.groupby('B_fighter').size().reset_index(name='B_counts')
    
    red_counts = red_counts.set_index('R_fighter')
    red_counts.index.names = ['fighter']
    
    blue_counts = blue_counts.set_index('B_fighter')
    blue_counts.index.names = ['fighter']

    fighter_counts = red_counts.merge(blue_counts, on='fighter')

    fighter_counts['num_fights'] = fighter_counts['R_counts'] + fighter_counts['B_counts']
    
    return fighter_counts

def get_fight_time(df):
    # function to get the total fight time in seconds for each fight
    #
    # df: DataFrame, contains fight data
    
    # convert from format 'xx:yy' to total number of seconds, e.g. 1:26 to 86
    df['last_round_secs'] = df['last_round_time'].map(lambda s: list(map(int, s.split(':')))).map(lambda x: x[0]*60 + x[1])
    
    df['total_time'] = 5*60*(df['last_round']-1) + df['last_round_secs']
    
    return df
