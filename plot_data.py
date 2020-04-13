import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import warnings
import pdb

from utils import *

# TODO: order columns from highest to lowest concentration (i.e. lighter colours
#  at the front of the plot)

def plot_heat_strikes(df, stk_type, width=19.20, height=10.8, fmt='.png',
                      rows_exc=['Catchweight', 'Openweight', 'NA'],
                      switch_ax=False):
    # function to plot heatmap of strikes per weight class, for landed or
    # attempted strikes
    #
    # df: DataFrame containing fight metrics
    # stk_type: str, one of ['landed', 'attempted']
    # width: int, width of the plot in inches (default is A4)
    # height: int, height of the plot in inches (default is A4)
    # fmt: str, file format (defaults to PNG)
    # rows_exc: lst of str, weight classes to exclude from the plot
    # switch_ax: Boolean, True if you want to switch the x and y axes on the plot
    
    p1 = 'Average Strikes '
    p2 = 'per 15 Minutes For Each Weight Class, by Strike Type'
    
    # define flag to filter columns by landed or attempted strikes
    if stk_type.upper() == 'LANDED':
        t = '_L'
        fname = './output/strikes-per-wc-landed' + fmt
        plt_title = p1 + 'Landed ' + p2
    elif stk_type.upper() == 'ATTEMPTED':
        t = '_A'
        fname = './output/strikes-per-wc-attempted' + fmt
        plt_title = p1 + 'Attempted ' + p2
    else:
        warnings.warn('Invalid strike type provided. Defaulting to "landed"')
        t = '_L'
        fname = './output/strikes-per-wc-landed' + fmt
        plt_title = p1 + 'Landed ' + p2

    # only keep the columns of the provided strike type
    df_heat = df.loc[:, list(map(lambda s: t in s, list(df.columns)))].copy()
    
    # only drop column if it exists
    for row in rows_exc:
        if row in df_heat.index:
            df_heat = df_heat.drop(row)
        else:
            continue
        
    df_heat = rename_cols(df_heat, list(df_heat.columns), 'strike', ['p15'])
    
    df_heat = df_heat.loc[:, df_heat.max().sort_values(ascending=False).index]
    
    if switch_ax:
        df_heat = df_heat.transpose()
    
    sns.set(rc={'figure.figsize':(width,height)})
    sns.set(font_scale=1.5)
    
    vmin = df_heat.values.min()
    vmax = df_heat.values.max()
    sns_plot = sns.heatmap(data=df_heat, annot=True, fmt='g', norm=LogNorm(vmin=vmin, vmax=vmax))
    plt.title(plt_title, fontsize=22)
    plt.yticks(rotation=0)
    
    # tighten the plot so it fits better
    plt.tight_layout()
    plt.axes().get_yaxis().get_label().set_visible(False)
    
    fig = sns_plot.get_figure()
    fig.savefig(fname)
