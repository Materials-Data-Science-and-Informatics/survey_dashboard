# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-9, Germany.               #
#                All rights reserved.                                         #
# This file is part of the survey_dashboard package.                          #
#                                                                             #
# The code is hosted on GitHub at                                             #
# https://github.com/Materials-Data-Science-and-Informatics/survey_dashboard  #
# For further information on the license, see the LICENSE file                #
###############################################################################
"""
This module contains functions to visualize data in an interactive way with mainly bokeh
"""
import numpy as np
from functools import wraps
from collections import Counter
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure as bokeh_figure
from bokeh.palettes import Category20c
#from bokeh.transform import factor_cmap
from bokeh.transform import cumsum
#from bokeh.models import FactorRange, Legend
#from bokeh.models import LinearColorMapper
#from bokeh.transform import transform
from bokeh.models import HelpTool
from bokeh.models import HoverTool
from bokeh.transform import dodge
from wordcloud import WordCloud
from bokeh.models import ColumnDataSource, Plot, Text
from PIL import ImageFont
from PIL import Image
from .analysis import percentage_to_area


DEFAULT_FIGURE_WIDTH = 600
ASPECT_RATIO = 4./3.
DEFAULT_FIGURE_HEIGHT = int(DEFAULT_FIGURE_WIDTH/ASPECT_RATIO) # functions expect an int

def add_legend_at(fig, position='right'):
    """
    Move/add a legend to the outside of a figure
    """
    #fig.legend.visible = False
    #legent_it = fig.legend.items
    #legend = Legend(items=legent_it)
    legend = fig.legend
    fig.add_layout(legend, position)
    return fig


# test
#df_test = pd.DataFrame(data=dict(value=xs[0], counts=ys[0]))
#fig = bokeh_barchart(df_test, factors=xs[0])
#show(fig)

# test2
#counts2 = sum(zip(*ys), ())
#factors = [(str(ques), ans) for ques in range(len(xs)) for ans in xs[0]] # factors have to be unique, and strings
#df_test3 = ColumnDataSource(data=dict(value=factors, counts=counts2))
#palette = Category20c[len(ys[0])]
#fig = bokeh_barchart(df_test3, factors=factors, fill_color=factor_cmap('value', palette=palette, factors=xs[0], start=1, end=2))
#show(fig)


default_theme = {
    "figure_kwargs" : {
    "background_fill_color" : '#00000000', #F7F7F7', #transparent
    "border_fill_color" : '#00000000',
    "x_range.range_padding": 0.1,
    "xgrid.grid_line_color": None,
    "xaxis.major_label_orientation": 1,
    "title.text_font_size": '18px',
    "yaxis.axis_label_text_font_size": '18px',
    "xaxis.axis_label_text_font_size": '18px',
    "xaxis.major_label_text_font_size": '16px',
    "yaxis.major_label_text_font_size": '16px',
    "toolbar.logo": None,
    "toolbar_location": "right",
    "legend.location": "top_right",
    "legend.orientation": "vertical",
    "legend.click_policy": "hide",
    "width": DEFAULT_FIGURE_WIDTH,
    "height": DEFAULT_FIGURE_HEIGHT}
}
corr_theme = {
    "figure_kwargs" : {
    "border_fill_color" : '#00000000',
    "background_fill_color" : '#00000000',
    "x_range.range_padding": 0.1,
    #"xgrid.grid_line_color": None,
    "xaxis.major_label_orientation": 1,
    "title.text_font_size": '18px',
    "yaxis.axis_label_text_font_size": '18px',
    "xaxis.axis_label_text_font_size": '18px',
    "xaxis.major_label_text_font_size": '16px',
    "yaxis.major_label_text_font_size": '16px',
    "toolbar.logo": None,
    "toolbar_location": "right",
    "legend.location": "top_right",
    "legend.orientation": "vertical",
    "legend.click_policy": "hide",
    "width": int(DEFAULT_FIGURE_WIDTH*1.5),
    "height": int(DEFAULT_FIGURE_HEIGHT*1.5)}
}




def apply_theme(theme=default_theme):
    """Decorator function to pre and post process a bokeh figure

    :param func: the function to be decorated
    :type func: function
    """
    def decorator(func):
        @wraps(func)
        def modified_plot(*args, **kwargs):
           """Modified plot functions"""
    
           # check if pandas data frame, if yes convert
           # pack figure_kwargs
           # set style?bokeh_barchart
           # plot function kwargs
    
           # before adjustments
           fig = func(*args, **kwargs)
           # after adjustments
           figure_kwargs = theme.get('figure_kwargs', {})
           for key, val in figure_kwargs.items():
                rek_set_attr(fig, key, val)
           return fig
        return modified_plot
    return decorator


def rek_set_attr(obj: object, key: str, val:object) -> None:
    """
    Recursively assigns to a given object and a key in dot notation a given value of any form

    Example: 
    1.
    rek_set_attr(figure, title, 'my-title')
    figure.title= 'my-title'
    2.
    rek_set_attr(figure, axis.xaxis.label.size, 10)
    figure.axis.xaxis.label.size = 10
    """
    if not '.' in key:
        return setattr(obj, key, val)
    else:
        keys = key.split('.')
        obj2 = getattr(obj, keys[0])
        key_new = ".".join(ke for ke in keys[1:])
        return rek_set_attr(obj2, key_new, val)




@apply_theme()
def bokeh_barchart(df, x='x_value', y=['y_value'], factors=None, figure=None, data_visible=[True], title='', 
                    width=0.1,  xlabel='', ylabel='Number of answers', palette=Category20c, 
                    fill_color=None, legend_labels=None, description='For more information about the HMC survey click here.', 
                    redirect='https://helmholtz-metadaten.de/en/',  orientation='vertical', x_range=None, y_range=None,**kwargs):
    """Create an interactive bar chart with bokeh

    :param df: [description]
    :type df: bokeh.models.ColumnDataSource
    :param x: [description], defaults to 'x_value'
    :type x: str, optional
    :param y: [description], defaults to ['y_value']
    :type y: list, optional
    :param factors: [description], defaults to None
    :type factors: [type], optional
    :param figure: [description], defaults to None
    :type figure: [type], optional
    :param data_visible: [description], defaults to [True]
    :type data_visible: list, optional
    :param title: [description], defaults to ''
    :type title: str, optional
    :param width: [description], defaults to 0.1
    :type width: float, optional
    :param xlabel: [description], defaults to ''
    :type xlabel: str, optional
    :param ylabel: [description], defaults to 'Number of answers'
    :type ylabel: str, optional
    :param palette: [description], defaults to Category20c
    :type palette: [type], optional
    :param fill_color: [description], defaults to None
    :type fill_color: [type], optional
    :param legend_labels: [description], defaults to None
    :type legend_labels: [type], optional
    :param description: [description], defaults to 'For more information about the HMC survey click here.'
    :type description: str, optional
    :param redirect: [description], defaults to 'https://helmholtz-metadaten.de/en/pages/structure-governance'
    :type redirect: str, optional
    :return: [description]
    :rtype: [type]
    """
    y_keys = y
    source = df
    #print(y, x)
    #print(df.column_names)
    help_t = HelpTool(description=description, redirect=redirect)
    tools = 'wheel_zoom,box_zoom,undo,reset,save'
    #if x_range is None:
    #    x_range = source.data[x]
    fig = bokeh_figure(x_range=x_range, y_range=y_range, title=title, #y_range=(0, 280), 
           height=DEFAULT_FIGURE_HEIGHT, width=DEFAULT_FIGURE_WIDTH, toolbar_location='above', tools=tools)

    fig.add_tools(help_t)
    
    nvisible = len(y_keys)
    step = width + 0.05
    if nvisible%2 == 0:
        start = -step*nvisible/2 + step/2.0
    elif nvisible==1:
        start = 0.0
    else:
        start = nvisible//2 * -step
    
    position = [start + i*step for i in range(len(y))]        
    tooltips=[(f'{x}', f'@{x}')]
    bars = []

    #for i, y in enumerate(y_keys):
    #    bar = fig.vbar(x=dodge(x, position[i], range=fig.x_range), top=y, source=source,
    #       width=width, color=fill_color[i], legend_label=y, **kwargs)
    for i, y in enumerate(y_keys):
        if orientation=='vertical':
            bar = fig.vbar(x=dodge(x, position[i], range=fig.x_range), top=y, source=source,
                width=width, color=fill_color[i], legend_label=y, selection_fill_color='black', 
                selection_fill_alpha=0.8,
                nonselection_fill_alpha=0.2,
                nonselection_fill_color="blue",
                selection_line_color="black", fill_alpha=0.8,
                nonselection_line_alpha=0.5, hover_fill_alpha=1.0,
                hover_line_color="black", hover_line_width=5.0, **kwargs)
            fig.y_range.start =  0
        else: # orientation=='horizontal':
            bar = fig.hbar(y=dodge(x, position[i], range=fig.y_range), right=y, source=source,
                height=width, color=fill_color[i], legend_label=y, selection_fill_color='black', selection_fill_alpha=0.8,
                nonselection_fill_alpha=0.2,
                nonselection_fill_color="blue",
                selection_line_color="black", fill_alpha=0.8,
                nonselection_line_alpha=0.5, hover_fill_alpha=1.0,
                hover_line_color="black", hover_line_width=5.0, **kwargs)   
            fig.x_range.start =  0

        tooltips.append((f'{y}', '@{' + str(y) + '}'))
        bars.append(bar)

    # How the data was given, there is not a way for the hover tool to display a single value
    hover = HoverTool(tooltips=tooltips,renderers=bars)
    fig.add_tools(hover)
    fig.yaxis.axis_label = ylabel
    fig.xaxis.axis_label = xlabel
    
    return fig

# bokeh piechart
@apply_theme()
def bokeh_piechart(df, x='x_value', y=['counts'], figure=None, outer_radius=0.7, inner_radius=0.4, 
                   title='', fill_color=None, legend_labels=None, line_color='black', **kwargs):
    """Draw an interactive piechart with bokeh
    
    using annular_wedge
    
    """
    # TODO refactor all the data processing out and create a plot interface for nested piechart.
    # This became way to specific...
    
    from math import pi
    plot_outer = False
    start_angle_inner = 'angle'
    start_angle_outer = 'angle'
    #if legend_labels is None: # must be string, given arry does not work
    #    legend_labels = x
    # The coloring has to be different now
    if 'All' in y:
        # If all is given, we use that as total
        ydata_all = np.array(df.data['All'])
        all_sum = sum(ydata_all)

    elif 'Cum. Sum' in y:
        # this becomes the total then
        ydata_all = np.array(df.data['All'])
        all_sum = sum(ydata_all)        
    else:
        all_sum = 0
        ydata_all = []
        for i, data in enumerate(df.data[y[0]]):
            ydata_sum = 0
            for key in y:
                # add up new total.
                ydata_sum = ydata_sum + np.array(df.data[key][i])
            ydata_all.append(ydata_sum)
            all_sum = all_sum + ydata_sum

    df.data['percent'] = ydata_all / all_sum
    df.data['count'] = ydata_all
    df.data['angle'] = ydata_all / all_sum * 2 * pi
    df.data['color_outer'] = ['#3182bd' for i in ydata_all] #light blue
    df.data['legend_field'] = ['Total' for i in ydata_all]
    
    y_clean = list(y) #copy list
    fill_color_outer = list(fill_color)
    legend_labels_clean = list(legend_labels)
    if 'All' in y_clean:
        index = y_clean.index('All')
        y_clean.remove('All')
        fill_color_outer.pop(index)
        legend_labels_clean.pop(index)
    if 'Cum. Sum' in y_clean:
        index = y_clean.index('Cum. Sum')
        y_clean.remove('Cum. Sum')
        fill_color_outer.pop(index)
        legend_labels_clean.pop(index)
    if len(y_clean)>1: # As soon as there is more then one different key do a nested chart
        ydata_outer = []
        data_outer_label = []
        data_outer_color = []
        hover_display = []
        plot_outer = True
        # data has to be resorted/matrix inverted
        # and filled with other, if All or cumsum is present...
        for i, data in enumerate(ydata_all):
            ydatasum = 0
            cat = df.data[x][i]
            for j, key in enumerate(y_clean):
                if key == 'All' or key == 'Cum. Sum':
                    continue
                ydata = df.data[key]
                ydata_outer.append(ydata[i])
                ydatasum = ydatasum + ydata[i]
                data_outer_color.append(fill_color_outer[j])
                data_outer_label.append(legend_labels_clean[j])
                hover_display.append(f'{cat}, {key}')# (Cat, Filter)
            if ydatasum < data:
                # fill rest with other
                diff = data - ydatasum
                ydata_outer.append(diff)
                data_outer_color.append('#f0f0f0')
                data_outer_label.append('Other') 
                hover_display.append(f'{cat}, Other')
        df_outer = ColumnDataSource()
        df_outer.data['percent'] = np.array(ydata_outer) / all_sum
        df_outer.data['angle'] = np.array(ydata_outer) / all_sum * 2 * pi
        df_outer.data['color'] = data_outer_color
        df_outer.data['labels'] = data_outer_label
        # for hover tool
        df_outer.data['count'] = np.array(ydata_outer)
        df_outer.data[x] = hover_display 


    tools = 'hover,wheel_zoom,box_zoom,undo,reset,save'
    if figure is None:
        fig = bokeh_figure(height=DEFAULT_FIGURE_HEIGHT, width=DEFAULT_FIGURE_WIDTH,
               title=title,
               toolbar_location='above',
               tools=tools,
               tooltips=[('Data', f'@{x}'),
                         ('Percentage', '@percent{0.00%}'), 
                         ('Count', f'@count')])
    else:
        fig = figure
        
    # As Legend labels total and areas
    # so it seems it has to be custom...
    #fig.add_layout(Legend(), 'right')
    # outer chart
    if not plot_outer:
        inner_radius = outer_radius
    fig.annular_wedge(x=0,
            y=1,
            inner_radius=0.0, 
            outer_radius=inner_radius,
            start_angle=cumsum(start_angle_inner, include_zero=True),
            end_angle=cumsum(start_angle_inner),
            line_color=line_color,
            fill_color='color_outer',
            legend_field='legend_field',
            source=df,
            selection_fill_color='black', selection_fill_alpha=1.0,
            nonselection_fill_alpha=0.2,
            nonselection_fill_color="blue",
            selection_line_color="black", fill_alpha=0.8,
            nonselection_line_alpha=0.5, hover_fill_alpha=1.0,
            hover_line_color="black", hover_line_width=5.0, **kwargs)
    
    # outer chart
    if plot_outer:
        fig.annular_wedge(x=0,
            y=1,
            inner_radius=inner_radius,# if we start from 0, hover tool highlight will be nice, but we get double hints
            outer_radius=outer_radius,
            start_angle=cumsum(start_angle_outer, include_zero=True),
            end_angle=cumsum(start_angle_outer),
            line_color=line_color,
            fill_color='color',
            legend_field='labels',
            source=df_outer,
            selection_fill_color='black', selection_fill_alpha=1.0,
            nonselection_fill_alpha=0.2,
            nonselection_fill_color="blue",
            selection_line_color="black", fill_alpha=0.8,
            nonselection_line_alpha=0.5, hover_fill_alpha=1.0,
            hover_line_color="black", hover_line_width=5.0, **kwargs)
        

    fig.toolbar.logo = None
    fig.axis.axis_label = None
    fig.axis.visible = False
    fig.grid.grid_line_color = None
    #fig.legend.location = "right"
    #fig.legend.orientation = "horizontal"
    #fig.legend.click_policy="hide"

    return fig


'''
# bokeh piechart
@apply_theme
def bokeh_piechart(df, x='x_value', y=['counts'], figure=None, outer_radius=0.6, inner_radius=0.4, 
                   title='', fill_color=None, legend_labels=None, line_color='black', **kwargs):
    """Draw an interactive piechart with bokeh
    
    using annular_wedge
    
    """
    # TODO refactor all the data processing out and create a plot interface for nested piechart.
    # This became way to specific...
    # Also a nice view is a sunburst, this could allow for further filter nesting...
    
    from math import pi
    plot_inner = False
    start_angle_inner = 'angle'
    start_angle_outer = 'angle'
    #if legend_labels is None: # must be string, given arry does not work
    #    legend_labels = x
    # The coloring has to be different now
    if 'All' in y:
        # If all is given, we use that as total
        ydata_all = np.array(df.data['All'])
        all_sum = sum(ydata_all)

    elif 'Cum. Sum' in y:
        # this becomes the total then
        ydata_all = np.array(df.data['All'])
        all_sum = sum(ydata_all)        
    else:
        all_sum = 0
        ydata_all = []
        for i, data in enumerate(df.data[y[0]]):
            ydata_sum = 0
            for key in y:
                # add up new total.
                ydata_sum = ydata_sum + np.array(df.data[key][i])
            ydata_all.append(ydata_sum)
            all_sum = all_sum + ydata_sum

    df.data['percent'] = ydata_all / all_sum
    df.data['count'] = ydata_all
    df.data['angle'] = ydata_all / all_sum * 2 * pi
    df.data['color_outer'] = ['#3182bd' for i in ydata_all] #light blue
    df.data['legend_field'] = ['Total' for i in ydata_all]
    
    y_clean = list(y) #copy list
    fill_color_inner = list(fill_color)
    legend_labels_clean = list(legend_labels)
    if 'All' in y_clean:
        index = y_clean.index('All')
        y_clean.remove('All')
        fill_color_inner.pop(index)
        legend_labels_clean.pop(index)
    if 'Cum. Sum' in y_clean:
        index = y_clean.index('Cum. Sum')
        y_clean.remove('Cum. Sum')
        fill_color_inner.pop(index)
        legend_labels_clean.pop(index)
    if len(y_clean)>1: # As soon as there is more then one different key do a nested chart
        ydata_inner = []
        data_inner_label = []
        data_inner_color = []
        hover_display = []
        plot_inner = True
        # data has to be resorted/matrix inverted
        # and filled with other, if All or cumsum is present...
        for i, data in enumerate(ydata_all):
            ydatasum = 0
            cat = df.data[x][i]
            for j, key in enumerate(y_clean):
                if key == 'All' or key == 'Cum. Sum':
                    continue
                ydata = df.data[key]
                ydata_inner.append(ydata[i])
                ydatasum = ydatasum + ydata[i]
                data_inner_color.append(fill_color_inner[j])
                data_inner_label.append(legend_labels_clean[j])
                hover_display.append(f'{cat}, {key}')# (Cat, Filter)
            if ydatasum < data:
                # fill rest with other
                diff = data - ydatasum
                ydata_inner.append(diff)
                data_inner_color.append('gray')
                data_inner_label.append('other') 
                hover_display.append(f'{cat}, other')
        df_inner = ColumnDataSource()
        df_inner.data['percent'] = np.array(ydata_inner) / all_sum
        df_inner.data['angle'] = np.array(ydata_inner) / all_sum * 2 * pi
        df_inner.data['color'] = data_inner_color
        df_inner.data['labels'] = data_inner_label
        # for hover tool
        df_inner.data['count'] = np.array(ydata_inner)
        df_inner.data[x] = hover_display
    tools = 'wheel_zoom,box_zoom,undo,reset,save,hover'
    if figure is None:
        fig = bokeh_figure(height=DEFAULT_FIGURE_HEIGHT, width=DEFAULT_FIGURE_WIDTH,
               title=title,
               toolbar_location='above',
               tools=tools,
               tooltips=[('Data', f'@{x}'),
                         ('Percent', '@percent{0.00%}'), 
                         ('Count', f'@count')])
    else:
        fig = figure
        
    # As Legend labels total and areas
    # so it seems it has to be custom...
    #fig.add_layout(Legend(), 'right')
    # outer chart
    if not plot_inner:
        inner_radius = 0.1
    fig.annular_wedge(x=0,
            y=1,
            inner_radius=inner_radius, # if we start from 0, hover tool highlight will be nice, but we get double hints
            outer_radius=outer_radius,
            start_angle=cumsum(start_angle_outer, include_zero=True),
            end_angle=cumsum(start_angle_outer),
            line_color=line_color,
            fill_color='color_outer',
            legend_field='legend_field',
            source=df,
            selection_fill_color='black', selection_fill_alpha=1.0,
            nonselection_fill_alpha=0.2,
            nonselection_fill_color="blue",
            selection_line_color="black", fill_alpha=0.8,
            nonselection_line_alpha=0.5, hover_fill_alpha=1.0,
            hover_line_color="black", hover_line_width=5.0, **kwargs)
    
    # inner chart
    if plot_inner:
        fig.annular_wedge(x=0,
            y=1,
            inner_radius=0.1,
            outer_radius=inner_radius,
            start_angle=cumsum(start_angle_inner, include_zero=True),
            end_angle=cumsum(start_angle_inner),
            line_color=line_color,
            fill_color='color',
            legend_field='labels',
            source=df_inner,
            selection_fill_color='black', selection_fill_alpha=1.0,
            nonselection_fill_alpha=0.2,
            nonselection_fill_color="blue",
            selection_line_color="black", fill_alpha=0.8,
            nonselection_line_alpha=0.5, hover_fill_alpha=1.0,
            hover_line_color="black", hover_line_width=5.0, **kwargs)
        

    fig.toolbar.logo = None
    fig.axis.axis_label = None
    fig.axis.visible = False
    fig.grid.grid_line_color = None
    #fig.legend.location = "right"
    #fig.legend.orientation = "horizontal"
    #fig.legend.click_policy="hide"

    return fig
'''
# test
#df_test = pd.DataFrame(data=dict(value=xs[0], counts=ys[0], xlabel=xs[0]))
#fig = bokeh_piechart(df_test)
#show(fig)

'''
@preprocess_bokeh_input
def bokeh_corr_plot(df, x='x_values', y='y_values',  figure=None, title='', markersize='markersize',  
xlabel='Answers', ylabel='Number of answers', alpha=None, **kwargs):
    """Plot an interactive circle with bokeh"""

    if figure is None:
        fig = bokeh_figure(height=600, width=600,
               title=title,
               toolbar_location='above',
               tools='',#'hover',
               tooltips=[('Data', f'@{x}'), ('Count', f'@{y}')])
    else:
        fig = figure
    if alpha is None:
        alpha = 1.0
    colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    mapper = LinearColorMapper(palette=colors, low=df.data[y].min(), high=df.data[y].max())   
    fig.circle(source=df, x=x, y=y, radius = 0.9, **kwargs)#size=markersize, fill_color={'field': 'region', 'transform': color_mapper}, fill_alpha=alpha)
    #line_color='#7c7e71',
    #line_width=0.5,
    #line_alpha=0.5,
    #legend_group='region')
    
    fig.y_range.start = 0
    fig.x_range.range_padding = 0.1
    fig.xaxis.major_label_orientation = 1
    #fig.xgrid.grid_line_color = None
    fig.yaxis.axis_label = ylabel
    fig.xaxis.axis_label = xlabel
    fig.toolbar.logo = None

    #fig.legend.location = "left"
    #fig.legend.orientation = "horizontal"
    #fig.legend.click_policy="hide"

    return fig

'''



@apply_theme(theme=corr_theme)
def bokeh_corr_plot(source, x='x_values', y='y_values',  figure=None, title='', x_range=None, y_range=None, 
                    markersize='markersize',  xlabel='', ylabel='', 
                    alpha=0.6, tooltips=None, leg_color='red', nleg_items=5 , **kwargs):
    """Plot an interactive circle with bokeh"""

    #TODO: make this work with Multiple choice, i.e multiple x, y given
    #TODO: make this work with 

    default_tooltips = [(f"{x}", "@x"), 
                    (f"{y}", "@y"),
                  ("Total", "@total"),
                  ("Percentage", "@percentage")]
    if tooltips is None:
        tooltips = default_tooltips


    fig = bokeh_figure(height=DEFAULT_FIGURE_HEIGHT, width=DEFAULT_FIGURE_WIDTH,
               title=title,
               toolbar_location='right',
               tools='hover,wheel_zoom,box_zoom,undo,reset,save',
                  y_range=y_range, x_range=x_range, tooltips=tooltips)

    circle = fig.circle(source=source, x=x, y=y, size=markersize, alpha=alpha, hover_alpha=1.0, 
           hover_line_color='black', hover_line_width=5, fill_color='color',  line_color='color', **kwargs)  #radius=0.1,
    
    fig.xaxis.major_label_orientation = 1
    fig.xaxis.axis_line_alpha= 0
    fig.yaxis.axis_line_alpha= 0
    fig.xgrid.grid_line_alpha = 1
    fig.ygrid.grid_line_alpha = 1
    fig.outline_line_color = None
    fig.yaxis.axis_label = ylabel
    fig.xaxis.axis_label = xlabel
    #fig.title.text_font_size='18px'
    #fig.yaxis.axis_label_text_font_size = '18px'
    #fig.xaxis.axis_label_text_font_size = '18px'
    #fig.xaxis.major_label_text_font_size = '16px'
    #fig.yaxis.major_label_text_font_size = '16px'
    #fig.toolbar.logo = None

    # Or draw legend by hand as in, i.e a new plot/figure with no axis and text
    # https://docs.bokeh.org/en/latest/docs/gallery/burtin.html
    # There was some work but declined: https://github.com/bokeh/bokeh/pull/10742
    # https://github.com/bokeh/bokeh/issues/2603
    #leg_colors = [leg_color for i in range(nleg_items)]
    #leg_items = create_legend_items(nleg_items, size_min=0, color=leg_colors, fig=fig) #[("circle", [circle])]
    #legend = Legend(
    #    title="Rel. amount\nof answers [%]",
    #    items=leg_items,
    #    location='top', orientation='vertical',
    #    border_line_color=None,
    #    title_text_font_size = '14px',
    #    title_text_font_style = 'bold'
    #)
    #fig.add_layout(legend, 'right')

    return fig
'''
def create_legend_items(number, size_min, color, fig):
    """
    """
    # TODO the size is not shown in the legend,... do not know how to do this.
    leg_items = []
    step = int(100/(number-1))
    size = size_min
    alpha_min = 0.2
    for i in range(number):
        circ = fig.circle(radius=size, x=0.0, y=0.0, muted=True, visible=False, fill_color=color[i], name='foo')
        leg_items.append((f'{size}', [circ]))
        size = size + step
    
    return leg_items
'''

def create_legend_items(number, size_min, color, fig, steps=None, data=None, scale_m=1.0, alpha=0.6):
    """
    This is the legend for a certain type of plot, Where the size of the circles corresponds to the 
    'precentage', i.e range from 0 to 100
    """
    if steps is None:
        if data is None:
            steps = [0,25,50,75,100]
        else:
            data_range = max(data)-min(data)
            # round to 5th
            steps = []

    leg_items = []
    #step = int(100/(number-1))
    #size = size_min
    alpha_min = 0.2
    x_offset = 5
    y_offset = -20
    y = y_offset
    y_step = int((fig.height+2*y_offset)/number)
    sizes = percentage_to_area(steps, scale_m=scale_m)
    for i in range(number):
        size = sizes[i]
        circ = fig.circle(size=size, x=3.0, y=y, fill_color=color[i], name='foo', alpha=alpha)
        txt = fig.text(text=[f'{steps[i]}'], x=3.0+x_offset, y=y, text_font_size="18px", 
                       text_align="left", text_baseline="middle")
        y = y - y_step
        #size = size + step
        leg_items.append(circ)
        leg_items.append(txt)
    return leg_items

def create_legend_corr(fig, colors=['red', 'blue', 'green', 'red', 'red', 'red'], 
    title="Rel. amount\nof answers [%]", width_ratio=5, scale_m=1.0):
    
    height = fig.height
    width = int(fig.width/width_ratio)
    fig2 = bokeh_figure(height=height, width=width,
               title=title,
               toolbar_location=None,
               tools='')
    leg_items = create_legend_items(5, size_min=0, color=colors, fig=fig2, scale_m=scale_m) #[("circle", [circle])]

    fig2.background_fill_color = '#00000000' #F7F7F7', #transparent
    fig2.border_fill_color = '#00000000'
    fig2.xaxis.axis_line_alpha= 0
    fig2.yaxis.axis_line_alpha= 0
    fig2.xgrid.grid_line_alpha = 0
    fig2.ygrid.grid_line_alpha = 0
    fig2.xaxis.axis_label_text_alpha = 0
    fig2.border_fill_alpha = 0
    fig2.xaxis.major_label_text_alpha = 0
    fig2.yaxis.major_label_text_alpha = 0
    fig2.x_range.start = 0.0
    fig2.x_range.end = 10.0
    fig2.y_range.start = -height
    fig2.y_range.end = 0.0
    fig2.xaxis.minor_tick_line_alpha = 0
    fig2.xaxis.major_tick_line_alpha = 0
    fig2.yaxis.minor_tick_line_alpha = 0
    fig2.yaxis.major_tick_line_alpha = 0
    fig2.outline_line_color = None
    
    return fig2


# Try to find an interactive wordcloud
def generate_wordcloud(word_list, min_font_size=5, max_font_size=50, max_words=100, background_color='white', **kwargs):
    """
    This returns a static svg image of the wordcloud

    """
    if len(word_list) == 0:
        # if no words are given, we at least return a wordcloud, importaant as palceholder
        word_list = ['Empty-word-cloud']
    word_count_dict = Counter(word_list)
    #text = "+".join(ent for ent in word_list)
    #print(text)
    wordcloud = WordCloud(max_font_size=max_font_size, min_font_size=min_font_size, max_words=max_words, background_color=background_color, **kwargs).generate_from_frequencies(word_count_dict)
    
    return wordcloud



def interactive_wordcloud(wordcloud, **kwargs):
    """
    Visualize a wordcloud

    :param wordcloud: the wordcloud instance 
    :type wordcloud: Wordcloud

    """
    wc = wordcloud
    data = {}
    height, width = wc.height*wc.scale, wc.width*wc.scale

    data_word, data_word_count, data_word_x, data_word_y, data_word_color, data_word_font_size,  data_word_angle= [],[],[],[],[],[], []
    # Get font information
    # Get max font size
    if wc.max_font_size is None:
        max_font_size = max(w[1] for w in wc.layout_)
    else:
        max_font_size = wc.max_font_size
    font = ImageFont.truetype(wc.font_path, int(max_font_size * wc.scale))
    raw_font_family, raw_font_style = font.getname()
    font_family = repr(raw_font_family)

    # The x and y ancor from the wordcloud is:
    # (0,0) is in the upper, left corner
    for (word, count), font_size, (y, x), orientation, color in wc.layout_:
        x *= wc.scale
        y *= wc.scale

        # Get text metrics
        font = ImageFont.truetype(wc.font_path, int(font_size * wc.scale))
        (size_x, size_y), (offset_x, offset_y) = font.font.getsize(word)
        ascent, descent = font.getmetrics()

        # Compute text bounding box
        min_x = -offset_x
        max_x = size_x - offset_x
        max_y = ascent - offset_y
        min_y = -offset_y


        if orientation == Image.ROTATE_90:
            angle = 90
            x += max_y
            y += max_x - min_x            
        else:
            angle = 0.0
            x += min_x
            y += max_y
        
        data_word.append(word)
        data_word_count.append(count)
        data_word_font_size.append(f'{font_size}px')
        data_word_x.append(x)
        data_word_y.append(-y)
        data_word_color.append(color)
        data_word_angle.append(angle)
        
    data = {'x': data_word_x,
            'y': data_word_y,
            'font_size' : data_word_font_size,
            'color' : data_word_color,
            'hover_color' : ['black' for i in data_word_color],
            'hover_font_size' : ['{}px'.format(int(size.split('px')[0])+5) for size in data_word_font_size],
            'text': data_word,
            'count' : data_word_count,
            'angle' : data_word_angle
           }
    source = ColumnDataSource(data=data)
    tools='hover,tap'#pan,box_zoom,wheel_zoom,save'

    # Maybe switch tooltip off, and register a callback to the size,
    # i.e. increase size on hover, or color black
    tooltips = [("", "@text")]#[(f"Word", "@text"), 
               # (f"Count", "@count")]#,
               #(f"X", "@x"),
               #(f"Y", "@y")]
    
    fig =  bokeh_figure(height=height, width=width,
               title='',
               toolbar_location=None,
               tools=tools,
               outline_line_color = None,
               x_axis_type= None, y_axis_type=None,#,
               tooltips=tooltips
            )
    glyph = Text(x="x", y="y", text="text", angle='angle', angle_units='deg', 
                 text_color="color", text_font_size='font_size', text_font={'value': font_family}, **kwargs)
    fig.add_glyph(source, glyph)
    
    fig.background_fill_color = '#00000000' #F7F7F7', #transparent
    fig.border_fill_color = '#00000000'
    return fig