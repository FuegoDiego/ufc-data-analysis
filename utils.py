import pandas as pd
import numpy as np
import json
import pdb

def get_corner_cols(df):
    # function to get the columns corresponding to each corner
    #
    # df: DataFrame, contains fight data
    
    red_corner = list(filter(lambda s: 'R_' in s, df.columns))
    blue_corner = list(filter(lambda s: 'B_' in s, df.columns))
    
    return red_corner, blue_corner

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

def rename_cols(df, cols):
    # function to rename column names to a more readable format
    #
    # df: DataFrame with columns cols to be renamed
    # cols: list of columns to be renamed
    
    # read in the column mapping to get the new column names
    col_dict = read_col_map()
    
    def map_col(col):
        col_split = col.split(sep='_')
        col_lst = list(map(lambda s: col_dict[s], col_split))
        col_rename = " ".join(col_lst)
        
        return col_rename
    
    cols_rename = list(map(lambda s: map_col(s), cols))
    
    rename_dict = {cols[i]: cols_rename[i] for i in range(len(cols))}
    
    df = df.rename(columns=rename_dict)
    
    return df
