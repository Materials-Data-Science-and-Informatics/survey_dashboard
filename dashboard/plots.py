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
This module contains functions to visualize data in an interactive way with bokeh
"""
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure as bokeh_figure
from bokeh.palettes import Category20c
from bokeh.transform import factor_cmap
from bokeh.transform import cumsum
from bokeh.models import FactorRange, Legend
from bokeh.models import LinearColorMapper
from bokeh.transform import transform
from bokeh.models import HelpTool
from bokeh.models import HoverTool
from bokeh.transform import dodge
from wordcloud import WordCloud
from .analysis import percentage_to_area

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
def preprocess_bokeh_input(func):
    """Decorator function to preprocess, modify any bokeh plotting functions

    :param func: the function to be decorated
    :type func: function
    """
    def modified_plot(*args, **kwargs):
       """Modifed plot functions"""

       # check if pandas data frame, if yes convert
       # pack figure_kwargs
       # set style?bokeh_barchart
       # plot function kwargs

       # before adjustments
       fig = func(*args, **kwargs)
       
       # after adjustments
       return fig

    return modified_plot


@preprocess_bokeh_input
def bokeh_barchart(df, x='x_value', y=['y_value'], factors=None, figure=None, data_visible=[True], title='', 
                    width=0.1,  xlabel='', ylabel='Number of answers', palette=Category20c, 
                    fill_color=None, legend_labels=None, description='For more information about the HMC survey click here.', 
                    redirect='https://helmholtz-metadaten.de/en/pages/structure-governance',  orientation='vertical', **kwargs):
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
    fig = bokeh_figure(x_range=source.data[x], title=title, #y_range=(0, 280), 
           height=550, width=1200, toolbar_location='above', tools=tools)

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
        else: # orientation=='horizontal':
            bar = fig.hbar(y=dodge(x, position[i], range=fig.y_range), right=y, source=source,
                width=width, color=fill_color[i], legend_label=y, selection_fill_color='black', selection_fill_alpha=0.8,
                nonselection_fill_alpha=0.2,
                nonselection_fill_color="blue",
                selection_line_color="black", fill_alpha=0.8,
                nonselection_line_alpha=0.5, hover_fill_alpha=1.0,
                hover_line_color="black", hover_line_width=5.0, **kwargs)   


        tooltips.append((f'{y}', '@{' + str(y) + '}'))
        bars.append(bar)

    # How the data was given, there is not a way for the hover tool to display a single value
    hover = HoverTool(tooltips=tooltips,renderers=bars)
    fig.add_tools(hover)    
    fig.x_range.range_padding = 0.1
    fig.xgrid.grid_line_color = None
    fig.legend.location = "top_left"
    fig.legend.orientation = "horizontal"
    fig.y_range.start = 0
    fig.xaxis.major_label_orientation = 1
    fig.yaxis.axis_label = ylabel
    fig.xaxis.axis_label = xlabel
    fig.title.text_font_size='25px'
    fig.yaxis.axis_label_text_font_size = '22px'
    fig.xaxis.axis_label_text_font_size = '22px'
    fig.xaxis.major_label_text_font_size = '18px'
    fig.yaxis.major_label_text_font_size = '18px'
    fig.toolbar.logo = None
    fig.legend.location = "top_right"
    fig.legend.orientation = "vertical"
    fig.legend.click_policy="hide"


    return fig



# bokeh piechart
@preprocess_bokeh_input 
def bokeh_piechart(df, x='value', y='counts', figure=None, radius=0.8, title='', **kwargs):
    """Draw an interactive piechart with bokeh"""
    
    from math import pi

    if isinstance(df, ColumnDataSource):
        ydata = df.data[y]
        if not 'color' in df.column_names:
            if not len(ydata) > 20:
                df.data['color'] = Category20c[len(ydata)] # ! if len(xdata)>20 this fails
    else:
        ydata = df[y]
        if not 'color' in df.columns:
            df['color'] = Category20c[len(ydata)] # ! if len(xdata)>20 this fails

    ydata = np.array(ydata)
    df.data['percent'] = ydata / sum(ydata)
    df.data['angle'] = ydata / sum(list(ydata)) * 2 * pi

    if figure is None:
        fig = bokeh_figure(height=600, width=600,
               title=title,
               toolbar_location='above',
               tools='',#hover',
               tooltips=[('Data', f'@{x}'),
                         ('Percent', '@percent{0.00%}'), 
                         ('Count', f'@{y}')])
    else:
        fig = figure
    #fig.add_layout(Legend(), 'right')
    fig.wedge(x=0,
            y=1,
            radius=radius,
            start_angle=cumsum('angle', include_zero=True),
            end_angle=cumsum('angle'),
            line_color='white',
            fill_color='color',
            legend_field=x,
            source=df,
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
    fig.legend.location = "right"
    #fig.legend.orientation = "horizontal"
    #fig.legend.click_policy="hide"

    return fig

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



@preprocess_bokeh_input
def bokeh_corr_plot(source, x='x_values', y='y_values',  figure=None, title='', x_range=None, y_range=None, 
                    markersize='markersize',  xlabel='', ylabel='', 
                    alpha=0.6, tooltips=None, leg_color='red', nleg_items=5 , **kwargs):
    """Plot an interactive circle with bokeh"""

    default_tooltips = [(f"{x}", "@x"), 
                    (f"{y}", "@y"),
                  ("total", "@total"),
                  ("percentage", "@percentage")]
    if tooltips is None:
        tooltips = default_tooltips


    fig = bokeh_figure(height=600, width=900,
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
    fig.title.text_font_size='25px'
    fig.yaxis.axis_label_text_font_size = '22px'
    fig.xaxis.axis_label_text_font_size = '22px'
    fig.xaxis.major_label_text_font_size = '18px'
    fig.yaxis.major_label_text_font_size = '18px'
    fig.toolbar.logo = None

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

def create_legend_corr(fig, colors=['red', 'blue', 'green', 'red', 'red', 'red'], width_ratio=5, scale_m=1.0):
    
    height = fig.height
    width = int(fig.width/width_ratio)
    fig2 = bokeh_figure(height=height, width=width,
               title="Rel. amount\nof answers [%]",
               toolbar_location=None,
               tools='')
    leg_items = create_legend_items(5, size_min=0, color=colors, fig=fig2, scale_m=scale_m) #[("circle", [circle])]

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
def generate_wordcloud(word_list, min_font_size=10, max_font_size= 50, max_words=100, background_color='white', **kwargs):
    """
    This returns a static svg image of the wordcloud

    """
    if len(word_list) == 0:
        # if no words are given, we at least return a wordcloud, importaant as palceholder
        word_list = ['Empty-word-cloud']

    text = "+".join(ent for ent in word_list)
    #print(text)
    wordcloud = WordCloud(max_font_size=max_font_size, max_words=max_words, background_color=background_color, **kwargs).generate(text)
    
    return wordcloud
