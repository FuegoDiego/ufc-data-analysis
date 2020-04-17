import pandas as pd
import numpy as np
import pdb

def GetNumStat(fight_stat, stat_type):
    # Function to get number of strikes/takedowns landed or attempted
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

def ReplaceAccStat(DF, cols):
    # function that replaces a column in DF of the form 'n of m' with two
    # columns: one for strikes/takedowns landed, and one for strikes/takedowns
    # attempted. The column is replaced for both red and blue corner fighters
    #
    # DF: DataFrame containing fight data
    # col: column to replace, e.g. SIG_STR.
    
    for col in cols:
        red_col = 'R_' + col
        blue_col = 'B_' + col
        
        GetNumStatWrapper = lambda col, stat_type: GetNumStat(np.array(DF[col]), stat_type)
        
        red_landed = GetNumStatWrapper(red_col, 'landed')
        red_attempted = GetNumStatWrapper(red_col, 'attempted')
        
        blue_landed = GetNumStatWrapper(blue_col, 'landed')
        blue_attempted = GetNumStatWrapper(blue_col, 'attempted')
        
        # new columns
        red_col_l = red_col + '_L'  # landed
        red_col_a = red_col + '_A'  # attempted
        blue_col_l = blue_col + '_L'
        blue_col_a = blue_col + '_A'
        
        DF[red_col_l] = red_landed
        DF[red_col_a] = red_attempted
        DF[blue_col_l] = blue_landed
        DF[blue_col_a] = blue_attempted
        
        del DF[red_col]
        del DF[blue_col]
    
def ReplacePctStat(DF, cols):
    # function that modifies columns in DF that contain a percentage as a 
    # string to a percentage as a float, e.g. '99%' to '99'
    #
    # DF: DataFrame containing fight data
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
        DF[col] = DF[col].apply(lambda s: s.strip('%'))

def GetWeightClass(s):
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
