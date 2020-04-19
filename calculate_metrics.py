import pandas as pd
import numpy as np
import pdb

from utils import *

def CalcAvgFight(DF, cols):
    # Function to calculate the averages per 15 minutes, per fighter
    #
    # DF: DataFrame, contains fight data
    #
    # Returns:
    #   FIGHT_AVG: DataFrame, contains average metrics per 15 minutes for each
    #       fighter across their careers
    
    col_dict = ReadColMapping()['weight class']    
    
    red_cols, blue_cols = GetCornerCols(DF)
    
    # we want to append the total time of the fight in seconds in order to
    # calculate the average per 15 minutes
    red_cols.extend(['total_time', 'weight_class'])
    blue_cols.extend(['total_time', 'weight_class'])
    
    RED_CORNER = DF[red_cols]
    BLUE_CORNER = DF[blue_cols]
    
    RED_CORNER.rename(columns={'R_fighter':'fighter'}, inplace=True)
    BLUE_CORNER.rename(columns={'B_fighter':'fighter'}, inplace=True)
    
    # we have to create new fighters for those who fight at multiple weight
    # classes, e.g. Jorge Masvidal fights and Lightweight and Welterweight
    # this way, the averages only count towards the weight class that the
    # fight happened at
    GetFighterByClass(RED_CORNER, col_dict)
    GetFighterByClass(BLUE_CORNER, col_dict)

    RED_CORNER_SUM = RED_CORNER.groupby('fighter').sum()
    BLUE_CORNER_SUM = BLUE_CORNER.groupby('fighter').sum()
    
    # we want to get the totals by combining the numbers from when a fighter
    # was in the red corner and when they were in the blue corner
    FIGHT_SUM = RED_CORNER_SUM.merge(BLUE_CORNER_SUM, on='fighter', how='outer')
    FIGHT_SUM = FIGHT_SUM.fillna(0)  # a fighter only fought in one corner ever

    # this is the total number of seconds a fighter spent fighting in their
    # careers
    FIGHT_TIME = FIGHT_SUM['total_time_x'] + FIGHT_SUM['total_time_y']
    FIGHT_TIME = FIGHT_TIME.reset_index(name='total_time')
    FIGHT_TIME = FIGHT_TIME.set_index('fighter')

    FIGHT_SUM = CalcFightSums(FIGHT_SUM, cols)
    
    cols_avg = list(map(lambda s: s + '_p15', FIGHT_SUM.columns))
    cols_sum = FIGHT_SUM.loc[:, FIGHT_SUM.columns != 'total_time'].columns.values
    cols_rename = {cols_sum[i]: cols_avg[i] for i in range(len(cols_sum))}

    FIGHT_SUM = FIGHT_SUM.join(FIGHT_TIME, on='fighter')
    
    # get the average per 15 minutes
    FIGHT_AVG = FIGHT_SUM.div(FIGHT_SUM['total_time'] / 60 / 15, axis=0)
    
    del FIGHT_AVG['total_time']
    
    FIGHT_AVG = FIGHT_AVG.rename(columns=cols_rename)
    
    return FIGHT_AVG


def CalcAvgPerClass(FIGHT_AVG, WEIGHT_CLASS, cols):
    # Function to calculate the average statistic per weight class, e.g.
    # average significant strikes landed and attempted per weight class
    #
    # Args:
    #   FIGHT_AVG: DataFrame, contains average fight metrics per fighter
    #   WEIGHT_CLASS: DataFrame, contains the weight class of each fighter
    #
    # Returns:
    #   WEIGHT_CLASS_AVG: DataFrame, contrains the average metrics per weight
    #       class

    FIGHT_AVG = FIGHT_AVG.merge(WEIGHT_CLASS[['fighter', 'weight_class']], on='fighter')

    WEIGHT_CLASS_AVG = FIGHT_AVG.groupby('weight_class').mean().round(2)
    
    return WEIGHT_CLASS_AVG


def CalcFightSums(DF, cols):
    # Function to get the total number of strikes, submissions, takedowns, etc.
    # in a fight
    #
    # DF: DataFrame, contains fight data
    # cols: list(str), list of column names to calculate totals for
    #
    # Return:
    #   DF_STAT: DataFrame, contains the total number of strikes, etc. in each
    #       fight
    
    # columns for landed and attempted
    red, blue = AppendCornerName(cols)
    total_l, total_a = AppendStrikeName(cols)
    red_l, red_a = AppendStrikeName(red)
    blue_l, blue_a = AppendStrikeName(blue)
    
    # columns to retrieve, and do calculations on
    cols_red = red_l + red_a
    cols_blue = blue_l + blue_a
    cols_total = total_l + total_a
    
    DF_STAT = pd.DataFrame(DF[cols_red].values + DF[cols_blue].values, index=DF.index,
                      columns=cols_total)
    
    return DF_STAT


def CalcFightTime(DF):
    # Function to get the total fight time in seconds for each fight
    #
    # Args:
    #   DF: DataFrame, contains fight data
    #
    # Returns:
    #   DF: DataFrame, contains new column with the total time in seconds for
    #       every fight
    
    # convert from format 'xx:yy' to total number of seconds, e.g. 1:26 to 86
    DF['last_round_secs'] = DF['last_round_time'].map(lambda s: list(map(int, s.split(':')))).map(lambda x: x[0]*60 + x[1])
    
    DF['total_time'] = 5*60*(DF['last_round']-1) + DF['last_round_secs']
    
    return DF


def CalcNumFights(DF):
    # Function to get the number of fights per fighter
    #
    # Args:
    #   DF: DataFrame, contains fight data
    #
    # Returns:
    #   FIGHT_COUNTS: DataFrame, contains number of fights per fighter
    
    FIGHT_COUNTS = DF[['R_fighter', 'B_fighter']]

    RED_COUNTS = FIGHT_COUNTS.groupby('R_fighter').size().reset_index(name='R_counts')
    BLUE_COUNTS = FIGHT_COUNTS.groupby('B_fighter').size().reset_index(name='B_counts')
    
    RED_COUNTS = RED_COUNTS.set_index('R_fighter')
    RED_COUNTS.index.names = ['fighter']
    
    BLUE_COUNTS = BLUE_COUNTS.set_index('B_fighter')
    BLUE_COUNTS.index.names = ['fighter']

    FIGHT_COUNTS = RED_COUNTS.merge(BLUE_COUNTS, on='fighter')

    FIGHT_COUNTS['num_fights'] = FIGHT_COUNTS['R_counts'] + FIGHT_COUNTS['B_counts']
    
    return FIGHT_COUNTS


def CalcNumFinish(DF, group_by, finish_type):
    # Function to calculate the number of finishes by finish type grouped by
    # the column(s) given by the argument 'group_by'
    #
    # Args:
    #   DF: DataFrame, contains fight statistics and information
    #   group_by: lst(str), list of column names to group the calculation by
    #   finish_type: str, type of finish
    #
    # Example:
    #   CalcNumFinish(FIGHTS, ['weight_class'], 'KO/TKO')
    #
    # Returns:
    #   FINISHES: DataFrame, contains the number of finishes for each group
    #       given by 'group_by'
    
    FINISHES = DF[DF['win_by'].str.contains(finish_type)].reset_index()

    FINISHES = FINISHES.groupby(group_by).size().reset_index(name='count')
    
    return FINISHES

