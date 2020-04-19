import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LogNorm
import warnings
import pdb

from utils import *

# created by Alex Aklson for the Coursera course "Data Visualization with Python"
def PlotWaffleChart(categories, values, height, width, colormap, fmt='.png', value_sign='', title='', fig_path=''):
    # Function to create a waffle chart
    #
    # Args:
    #   categories: Unique categories or classes in dataframe.
    #   values: Values corresponding to categories or classes.
    #   height: Defined height of waffle chart.
    #   width: Defined width of waffle chart.
    #   colormap: Colormap class
    #   fmt: str, format of the image file
    #   value_sign: In order to make our function more generalizable, we will add
    #       this parameter to address signs that could be associated with a value
    #       such as %, $, and so on. value_sign has a default value of empty string.
    #
    # Returns:
    #   fig: figure object containing the waffle chart
    #   fig_path: str, path to save image to
    
    #       compute the proportion of each category with respect to the total
    total_values = sum(values)
    category_proportions = [(float(value) / total_values) for value in values]

    # compute the total number of tiles
    total_num_tiles = width * height # total number of tiles
    #print ('Total number of tiles is', total_num_tiles)
    
    # compute the number of tiles for each catagory
    tiles_per_category = [round(proportion * total_num_tiles) for proportion in category_proportions]

    # print out number of tiles per category
    #for i, tiles in enumerate(tiles_per_category):
    #    print (categories[i] + ': ' + str(tiles))
    
    # initialize the waffle chart as an empty matrix
    waffle_chart = np.zeros((height, width))

    # define indices to loop through waffle chart
    category_index = 0
    tile_index = 0

    # populate the waffle chart
    for col in range(width):
        for row in range(height):
            tile_index += 1

            # if the number of tiles populated for the current category 
            # is equal to its corresponding allocated tiles...
            if tile_index > sum(tiles_per_category[0:category_index]):
                # ...proceed to the next category
                category_index += 1       
            
            # set the class value to an integer, which increases with class
            waffle_chart[row, col] = category_index
    
    # instantiate a new figure object
    fig = plt.figure()

    # use matshow to display the waffle chart
    plt.matshow(waffle_chart, cmap=colormap)

    # get the axis
    ax = plt.gca()

    # set minor ticks
    ax.set_xticks(np.arange(-.5, (width), 1), minor=True)
    ax.set_yticks(np.arange(-.5, (height), 1), minor=True)
    
    # add dridlines based on minor ticks
    ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

    plt.xticks([])
    plt.yticks([])

    # compute cumulative sum of individual categories to match color schemes between chart and legend
    values_cumsum = np.cumsum(values)
    total_values = values_cumsum[len(values_cumsum) - 1]

    # create legend
    legend_handles = []
    for i, category in enumerate(categories):
        label_str = category + ' (' + str(values[i]) + ')'
        color_val = colormap(float(i)/(len(categories)-1))
        legend_handles.append(mpatches.Patch(color=color_val, label=label_str))

    # add legend to chart
    lgd=plt.legend(
        handles=legend_handles,
        loc='upper right',
        #bbox_to_anchor=(0,1.03)
        bbox_to_anchor=(1.22,1.03)
    )
    
    # set title
    plt.title(title, fontsize=22)
    
    if len(fig_path) != 0:
        fig_path = fig_path + fmt
        plt.savefig(fig_path, bbox_extra_artists=(lgd,), bbox_inches='tight')
    
    return fig


def PlotHeatStrikes(DF, stk_type, width=19.20, height=10.8, fmt='.png',
                      rows_exc=['Catchweight', 'Openweight', 'NA'],
                      switch_ax=False):
    # Function to plot heatmap of strikes per weight class, for landed or
    # attempted strikes
    #
    # Args:
    #   DF: DataFrame containing fight metrics
    #   stk_type: str, one of ['landed', 'attempted']
    #   width: int, width of the plot in inches (default is A4)
    #   height: int, height of the plot in inches (default is A4)
    #   fmt: str, file format (defaults to PNG)
    #   rows_exc: lst of str, weight classes to exclude from the plot
    #   switch_ax: Boolean, True if you want to switch the x and y axes on the plot
    #
    # Returns:
    #   fig: figure object containing heat map
    #   fig_path: str, figure path to save image to
    
    p1 = 'Average Strikes '
    p2 = 'per 15 Minutes For Each Weight Class, by Strike Type'
    
    # define flag to filter columns by landed or attempted strikes
    if stk_type.upper() == 'LANDED':
        t = '_L'
        fig_path = './output/strikes-per-wc-landed' + fmt
        plt_title = p1 + 'Landed ' + p2
    elif stk_type.upper() == 'ATTEMPTED':
        t = '_A'
        fig_path = './output/strikes-per-wc-attempted' + fmt
        plt_title = p1 + 'Attempted ' + p2
    else:
        warnings.warn('Invalid strike type provided. Defaulting to "landed"')
        t = '_L'
        fig_path = './output/strikes-per-wc-landed' + fmt
        plt_title = p1 + 'Landed ' + p2

    # only keep the columns of the provided strike type
    DF_HEAT = DF.loc[:, list(map(lambda s: t in s, list(DF.columns)))].copy()
    
    # only drop column if it exists
    for row in rows_exc:
        if row in DF_HEAT.index:
            DF_HEAT = DF_HEAT.drop(row)
        else:
            continue
        
    RenameColPlot(DF_HEAT, list(DF_HEAT.columns), 'strike', ['p15'])
    
    # sort so we can show the highest values first
    DF_HEAT = DF_HEAT.loc[:, DF_HEAT.max().sort_values(ascending=False).index]
    
    if switch_ax:
        DF_HEAT = DF_HEAT.transpose()
    
    sns.set(rc={'figure.figsize':(width,height)})
    sns.set(font_scale=1.5)
    
    vmin = DF_HEAT.values.min()
    vmax = DF_HEAT.values.max()
    sns_plot = sns.heatmap(data=DF_HEAT, annot=True, fmt='g', norm=LogNorm(vmin=vmin, vmax=vmax))
    plt.title(plt_title, fontsize=22)
    plt.yticks(rotation=0)
    
    # tighten the plot so it fits better
    plt.tight_layout()
    plt.axes().get_yaxis().get_label().set_visible(False)
    
    fig = sns_plot.get_figure()
    
    return fig, fig_path

