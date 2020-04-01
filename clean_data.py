import pandas as pd
import numpy as np
import pdb

def get_stat_num(fight_stat, stat_type):
    # function to get number of strikes/takedowns landed or attempted
    #
    # fight_stat: array of strings that contain a strike or takedown statistic
    #   for example, '33 of 45' which means 33 landed of 45 attempted
    # stat_type: one of 'landed', 'attempted'
    if stat_type == 'landed':
        idx = 0
    else:
        idx = 2
    fight_stat_map = np.array(list(map(lambda x: int(x.split()[idx]), fight_stat)))
    
    return fight_stat_map

def replace_acc_stat(df, cols):
    # function that replaces a column in df of the form 'n of m' with two
    # columns: one for strikes/takedowns landed, and one for strikes/takedowns
    # attempted. The column is replaced for both red and blue corner fighters
    #
    # df: DataFrame containing fight data
    # col: column to replace, e.g. SIG_STR.
    
    for col in cols:
        red_col = 'R_' + col
        blue_col = 'B_' + col
        
        get_stat_num_wrapper = lambda col, stat_type: get_stat_num(np.array(df[col]), stat_type)
        
        red_landed = get_stat_num_wrapper(red_col, 'landed')
        red_attempted = get_stat_num_wrapper(red_col, 'attempted')
        
        blue_landed = get_stat_num_wrapper(blue_col, 'landed')
        blue_attempted = get_stat_num_wrapper(blue_col, 'attempted')
        
        # new columns
        red_col_l = red_col + '_L'  # landed
        red_col_a = red_col + '_A'  # attempted
        blue_col_l = blue_col + '_L'
        blue_col_a = blue_col + '_A'
        
        df[red_col_l] = red_landed
        df[red_col_a] = red_attempted
        df[blue_col_l] = blue_landed
        df[blue_col_a] = blue_attempted
        
        del df[red_col]
        del df[blue_col]
    
def replace_pct_stat(df, cols):
    # function that modifies columns in df that contain a percentage as a 
    # string to a percentage as a float, e.g. '99%' to '99'
    #
    # df: DataFrame containing fight data
    # cols: list or set of columns to be modified

    # list of red and blue corner columns to be modified
    cnr_cols = []
    
    # append corner to column names
    for col in cols:
        red_cnr = 'R_' + col
        blue_cnr = 'B_' + col
        cnr_cols.append(red_cnr)
        cnr_cols.append(blue_cnr)

    for col in cnr_cols:
        df[col] = df[col].apply(lambda s: s.strip('%'))

def get_weight_class(s):
    # function to get the weight class from a string containing the Fight_type
    #
    # s: string containing Fight_type information, e.g. 'Lightweight Bout'
    
    s_split = s.split()
    
    sub_lst = ['weight', 'Catch', 'Open', "Women's", 'Light']
    
    weight_class = list(filter(lambda s: any(sub_str in s for sub_str in sub_lst), s_split))
    
    if len(weight_class) == 0:
        weight_class = 'NA'
    else:
        if weight_class[0] in ['Catch', 'Open']:
            weight_class = weight_class[0] + 'weight'
        elif "Women's" in weight_class:
            if weight_class[0] == "Women's":
                weight_class = weight_class[0] + ' ' + weight_class[1]
            else:
                weight_class = weight_class[1] + ' ' + weight_class[0]
        elif 'Light' in weight_class:
            if weight_class[0] == 'Light':
                weight_class = weight_class[0] + ' ' + weight_class[1]
            else:
                weight_class = weight_class[1] + ' ' + weight_class[0]
        else:
            weight_class = weight_class[0]
    
    return weight_class
