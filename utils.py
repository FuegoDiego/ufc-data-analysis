import pandas as pd
import numpy as np
import json
import pdb

def GetFighterByClass(DF, col_dict):
    # Function to create 'new' fighters with their weight class appended at the
    # end of a fighter's name. This is done to account for the fact that a
    # fighter might have fights at different weight classes
    #
    # Args:
    #   DF: DataFrame, contains fighter and weight class information
    
    DF.loc[:, ('weight_class_abv')] = DF.loc[:, ('weight_class')].map(lambda s: col_dict[s])
    
    DF.loc[:, ('fighter_wc')] = DF.loc[:, ('fighter')] + '_' + DF.loc[:, ('weight_class_abv')]
    
    del DF['weight_class_abv']
    
    DF.rename(columns={'fighter':'fighter_orig', 'fighter_wc':'fighter'}, inplace=True)

def GetCornerCols(DF):
    # Function to get the columns corresponding to each corner only, i.e.
    #   filter out every column that does not represent a statistic for one of
    #   the corners
    #
    # Args:
    #   DF: DataFrame, contains fight data
    #
    # Returns:
    #   red_cols: list(str), list of columns that correspond to the red corner
    #   blue_cols: list(str), list of columns that correspond to the blue corner
    
    red_cols = list(filter(lambda s: 'R_' in s, DF.columns))
    blue_cols = list(filter(lambda s: 'B_' in s, DF.columns))
    
    return red_cols, blue_cols

def GetClassFromFighter(DF):
    # Function to get the weight class of each fighter, taking into account 
    # that fighters sometimes fight at different weight classes
    #
    # Args:
    #   DF: DataFrame, contains fighter column of format fighter_wc, e.g.
    #       "Yoel Romero_MW"
    #
    # Returns:
    #   DF: DataFrame, contains new column with the weight class of each fighter
    
    col_dict = ReadColMapping()['weight class']
    inv_col_dict = {value: key for key, value in col_dict.items()}
    
    t = list(map(lambda s: s.split('_'), DF['fighter']))
    
    DF[['fighter_orig', 'weight_class_abv']] = pd.DataFrame(t)
    
    DF['weight_class'] = DF['weight_class_abv'].map(lambda s: inv_col_dict[s])
    
    return DF  

def AppendCornerName(cols):
    # Function to assign red and blue corner prefix to a column name
    #
    # Args:
    #   cols: list(str), column names
    #
    # Returns:
    #   red_cols: list(str), list of column names that correspond to the red corner
    #   blue_cols: list(str), list of column names that correspond to the blue corner
    
    red_cols = list(map(lambda s: 'R_' + s, cols))
    blue_cols = list(map(lambda s: 'B_' + s, cols))
    
    return red_cols, blue_cols

def AppendStrikeName(cols):
    # Function to assign landed and attempted prefix to a column name
    #
    # Args:
    #   cols: list(str), column names
    #
    # Returns:
    #   landed_cols: list(str), list of column names that correspond to landed
    #       strikes, submissions, etc.
    #   attempted_cols: list(str), list of column names that correspond to attempted
    #       strikes, submissions, etc.
    
    landed_cols = list(map(lambda s: s + '_L', cols))
    attempted_cols = list(map(lambda s: s + '_A', cols))
    
    return landed_cols, attempted_cols

def ReadColMapping(path='./column_mapping.json'):
    # Function to read in the column mapping JSON file as a dictionary
    #
    # Args:
    #   path: string specifying the file path to the JSON file
    #
    # Returns:
    #   data: JSON object that contains the column mappings
    
    with open(path) as f:
        data = json.load(f)
    
    return data

def RenameColPlot(DF, cols, col_type, sub_ignore=[]):
    # Function to rename column names to a more readable format for plotting
    #
    # Args:
    #   DF: DataFrame with columns cols to be renamed
    #   cols: list of columns to be renamed
    #   col_type: str, which type to rename, e.g. strike or weight class columns
    #   sub_ingore: list(str), list of substrings to ignore, e.g. 'p15'
    
    # read in the column mapping to get the new column names
    col_dict = ReadColMapping()

    def map_col(col):
        col_split = col.split(sep='_')
        col_split = [s for s in col_split if s not in sub_ignore]
        col_lst = list(map(lambda s: col_dict[col_type][s], col_split))
        col_rename = " ".join(col_lst)
        
        return col_rename
    
    cols_rename = list(map(lambda s: map_col(s), cols))
    
    rename_dict = {cols[i]: cols_rename[i] for i in range(len(cols))}
    
    DF.rename(columns=rename_dict, inplace=True)
