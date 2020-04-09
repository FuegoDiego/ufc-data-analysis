import pandas as pd
import numpy as np
import json
import pdb

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

def name_corner(cols):
    # function to assign red and blue corner prefix to a column name
    #
    # cols: numpy.array(str), column names
    
    red_corner = 'R_' + cols
    blue_corner = 'B_' + cols
    
    return red_corner, blue_corner

def name_lnd_att(cols):
    # function to assign landed and attempted prefix to a column name
    #
    # cols: numpy.array(str), column names
    
    landed = col + '_L'
    attempted = col + '_A'
    
    return landed, attempted
    

