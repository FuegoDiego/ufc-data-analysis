import pandas as pd
import numpy as np
import json
import pdb

def create_by_wc(df, col_dict):
    
    #fw = df.loc[:, ['fighter', 'weight_class']]
    
    #df = df[['fighter', 'weight_class']].drop_duplicates()
    
    df['weight_class_abv'] = df['weight_class'].map(lambda s: col_dict[s])
    
    df['fighter_wc'] = df['fighter'] + '_' + df['weight_class_abv']
    
    del df['weight_class_abv']
    #del df['fighter']
    
    df = df.rename(columns={'fighter':'fighter_orig', 'fighter_wc':'fighter'})
    
    return df

def get_corner_cols(df):
    # function to get the columns corresponding to each corner
    #
    # df: DataFrame, contains fight data
    
    red_corner = list(filter(lambda s: 'R_' in s, df.columns))
    blue_corner = list(filter(lambda s: 'B_' in s, df.columns))
    
    return red_corner, blue_corner

def create_weight_class(df):
    # get the weight class of each fighter, taking into account that fighters
    # sometimes fight at different weight classes
    #
    # df: DataFrame, contains fighter column of format fighter_wc, e.g.
    #   "Yoel Romero_MW"
    
    col_dict = read_col_map()['weight class']
    inv_col_dict = {value: key for key, value in col_dict.items()}
    
    t = list(map(lambda s: s.split('_'), df['fighter']))
    
    df[['fighter_orig', 'weight_class_abv']] = pd.DataFrame(t)
    
    df['weight_class'] = df['weight_class_abv'].map(lambda s: inv_col_dict[s])
    
    return df    

def name_corner(cols):
    # function to assign red and blue corner prefix to a column name
    #
    # cols: list(str), column names
    
    red_corner = list(map(lambda s: 'R_' + s, cols))
    blue_corner = list(map(lambda s: 'B_' + s, cols))
    
    return red_corner, blue_corner

def name_lnd_att(cols):
    # function to assign landed and attempted prefix to a column name
    #
    # cols: list(str), column names
    
    landed = list(map(lambda s: s + '_L', cols))
    attempted = list(map(lambda s: s + '_A', cols))
    
    return landed, attempted

def read_col_map(path='./column_mapping.json'):
    # function to read in the column mapping JSON file as a dictionary
    #
    # path: string specifying the file path to the JSON file
    
    with open(path) as f:
        data = json.load(f)
    
    return data

def rename_cols(df, cols, col_type, sub_ignore=[]):
    # function to rename column names to a more readable format
    #
    # df: DataFrame with columns cols to be renamed
    # cols: list of columns to be renamed
    # col_type: str, which type to rename, e.g. strike or weight class columns
    # sub_ingore: list(str), list of substrings to ignore, e.g. 'p15'
    
    # read in the column mapping to get the new column names
    col_dict = read_col_map()

    def map_col(col):
        col_split = col.split(sep='_')
        col_split = [s for s in col_split if s not in sub_ignore]
        col_lst = list(map(lambda s: col_dict[col_type][s], col_split))
        col_rename = " ".join(col_lst)
        
        return col_rename
    
    cols_rename = list(map(lambda s: map_col(s), cols))
    
    rename_dict = {cols[i]: cols_rename[i] for i in range(len(cols))}
    
    df = df.rename(columns=rename_dict)
    
    return df
