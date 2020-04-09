import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import pdb

from utils import *

# TODO: order columns from highest to lowest concentration (i.e. lighter colours
#  at the front of the plot)

def plot_heat_strikes(df, stk_type, width=11.69, height=8.24, fmt='.png',
                      rows_exc=['Catchweight', 'Openweight', 'NA']):
    # function to plot heatmap of strikes per weight class, for landed or
    # attempted strikes
    #
    # df: DataFrame containing fight metrics
    # stk_type: str, one of ['landed', 'attempted']
    # width: int, width of the plot in inches (default is A4)
    # height: int, height of the plot in inches (default is A4)
    # fmt: str, file format (defaults to PNG)
    # rows_exc: lst of str, weight classes to exclude from the plot
    
    # define flag to filter columns by landed or attempted strikes
    if stk_type.upper() == 'LANDED':
        t = '_L'
        fname = './output/strikes-per-wc-landed' + fmt
        plt_title = 'Average Strikes ' + 'Landed ' + 'For Each Weight Class, by Strike Type'
    elif stk_type.upper() == 'ATTEMPTED':
        t = '_A'
        fname = './output/strikes-per-wc-attempted' + fmt
        plt_title = 'Average Strikes ' + 'Attempted ' + 'For Each Weight Class, by Strike Type'
    else:
        warnings.warn('Invalid strike type provided. Defaulting to "landed"')
        t = '_L'
        fname = './output/strikes-per-wc-landed' + fmt
        plt_title = 'Average Strikes ' + 'Landed ' + 'For Each Weight Class, by Strike Type'

    # only keep the columns of the provided strike type
    df_heat = df.loc[:, list(map(lambda s: t in s, list(df.columns)))].copy()
    
    # only drop column if it exists
    for row in rows_exc:
        if row in df_heat.index:
            df_heat = df_heat.drop(row)
        else:
            continue
        
    df_heat = rename_cols(df_heat, list(df_heat.columns))
    
    sns.set(rc={'figure.figsize':(width,height)})
    
    sns_plot = sns.heatmap(data=df_heat, annot=True, fmt='g')
    plt.title(plt_title)
    plt.yticks(rotation=0)
    
    # tighten the plot so it fits better
    plt.tight_layout()
    plt.axes().axes.get_yaxis().get_label().set_visible(False)
    
    fig = sns_plot.get_figure()
    fig.savefig(fname)
