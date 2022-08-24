
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

# for tests
#import pandas as pd
#import random
#from bokeh.io import output_notebook, show, push_notebook

#x = [str(i) for i in range(7)]
#xs = [x,x,x,x,x]
#xlabels = [[f'1 pli bla blub {i}' for i in x], [f'2 pli bla blub {i}' for i in x], [f'3 pli bla blub {i}' for i in x], [f'4 pli bla blub {i}' for i in x], [f'5 pli bla blub {i}' for i in x]]
#ys = [[random.randint(0, 1200) for i in x], [random.randint(0, 1200) for i in x], [random.randint(0, 1200) for i in x],[random.randint(0, 1200) for i in x], [random.randint(0, 1200) for i in x]]

# bokeh bar plot
'''
def bokeh_barchart(df, x='value', y='counts', factors=None, figure=None, title='This is a title', width=0.9,  xlabel='Answers', ylabel='Number of answers', palette=Category20c, fill_color='color', description='For more information about the HMC survey click here.', redirect='https://helmholtz-metadaten.de/en/pages/structure-governance'):
    """Plot an interactive bar chart with bokeh"""
    legend_it = []
    if isinstance(df, ColumnDataSource):
        xdata = df.data[x]
        if not 'color' in df.column_names:
            if not len(xdata) > 20:
                df.data['color'] = Category20c[len(xdata)] # ! if len(xdata)>20 this fails
    else:
        xdata = df[x]
        if not 'color' in df.columns:
            df['color'] = Category20c[len(xdata)] # ! if len(xdata)>20 this fails
    
    help_t = HelpTool(description=description, redirect=redirect)

    tools = 'hover,wheel_zoom,box_zoom,undo,reset,save'
    if figure is None:
        if factors is not None:
            fig = bokeh_figure(plot_height=600, plot_width=600,
               title=title,
               toolbar_location='above',
               x_range=FactorRange(factors=factors),
               tools=tools,#'hover',
               tooltips=[('Data', f'@{x}'), ('Count', f'@{y}')])
        else:
            fig = bokeh_figure(plot_height=600, plot_width=600,
               title=title,
               toolbar_location='above',
               tools=tools,#'hover',
               tooltips=[('Data', f'@{x}'), ('Count', f'@{y}')])
    else:
        fig = figure
    #if factors is not None:
    #    fig.x_range=FactorRange(factors=factors)
    
    fig.add_tools(help_t)
    fig.vbar(x=x, top=y, width=width, source=df, line_color="white", fill_color=fill_color)#factor_cmap('x', palette=palette, factors=factors, start=1, end=2))
    fig.y_range.start = 0
    fig.x_range.range_padding = 0.1
    fig.toolbar.logo = None
    fig.xaxis.major_label_orientation = 1
    fig.xgrid.grid_line_color = None
    fig.yaxis.axis_label = ylabel
    fig.xaxis.axis_label = xlabel
    fig.xgrid.grid_line_color = None


    #fig.legend.location = "left"
    #fig.legend.orientation = "horizontal"
    #fig.legend.click_policy="hide"

    return fig

def bokeh_barchart2(df, x=['value'], y=['counts'], factors=None, figure=None, data_visible=[True], title='', width=0.9,  xlabel='Answers', ylabel='Number of answers', palette=Category20c, fill_color='color', legend_labels=None):
    """Plot an interactive bar chart with bokeh"""

    if figure is None:
        if factors is not None:
            fig = bokeh_figure(plot_height=600, plot_width=600,
               title=title,
               toolbar_location='above',
               #x_range=FactorRange(factors=factors),
               tools='',#'hover',
               tooltips=[('Data', f'@{x}'), ('Count', f'@{y}')])
        else:
            fig = bokeh_figure(plot_height=600, plot_width=600,
               title=title,
               toolbar_location='above',
               tools='',#'hover',
               tooltips=[('Data', f'@{x}'), ('Count', f'@{y}')])
    else:
        fig = figure
    
    if isinstance(x, list):
        if not 'color' in df.column_names:
            if isinstance(palette, dict):
                x_color = palette[len(x)]
        else:
            x_color = df.data['color']
        position = []
        step = width + 0.05
        nvisible = data_visible.count(True)
        if nvisible%2 == 0:
            start = -step*nvisible/2 + step/2.0
        elif nvisible==1:
            start = 0.0
        else:
            start = nvisible//2 * -step
        displayed_pos = [start + i*step for i in range(nvisible)]
        ind = 0
        for visible in data_visible:
            if not visible:
                position.append(0.0)
            else:
                position.append(displayed_pos[ind])
                ind = ind+1
        for i, data in enumerate(x):
            fig.vbar(x=dodge(data, position[i], range=fig.x_range), top=y[i], source=df,
                   width=width, color=x_color[i], legend_label=data, visible=data_visible[i])
    else:
        if isinstance(df, ColumnDataSource):
            xdata = df.data[x]
            if not 'color' in df.column_names:
                df.data['color'] = palette[len(xdata)]
        else:
            xdata = df[x]
            if not 'color' in df.columns:
                df['color'] = palette[len(xdata)]
        fig.vbar(x=x, top=y, width=width, source=df, line_color="white", fill_color=fill_color)#factor_cmap('x', palette=palette, factors=factors, start=1, end=2))
    
    fig.y_range.start = 0
    fig.x_range.range_padding = 0.1
    fig.xaxis.major_label_orientation = 1
    fig.xgrid.grid_line_color = None
    fig.yaxis.axis_label = ylabel
    fig.xaxis.axis_label = xlabel
    fig.xgrid.grid_line_color = None

    fig.toolbar.logo = None
    #fig.legend.location = "left"
    #fig.legend.orientation = "horizontal"
    #fig.legend.click_policy="hide"

    return fig
'''

def add_legend_outside(fig):
    """
    Move legend to the outside of a figure
    """
    #fig.legend.visible = False
    #legent_it = fig.legend.items
    #legend = Legend(items=legent_it)
    legend = fig.legend
    fig.add_layout(legend, 'right')
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


def bokeh_barchart(df, x='x_value', y=['y_value'], factors=None, figure=None, data_visible=[True], title='', 
                    width=0.1,  xlabel='', ylabel='Number of answers', palette=Category20c, 
                    fill_color=None, legend_labels=None, description='For more information about the HMC survey click here.', redirect='https://helmholtz-metadaten.de/en/pages/structure-governance'):
    y_keys = y
    source = df

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
    for i, y in enumerate(y_keys):
        bar = fig.vbar(x=dodge(x, position[i], range=fig.x_range), top=y, source=source,
           width=width, color=fill_color[i], legend_label=y)
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
    fig.toolbar.logo = None
    fig.legend.location = "top_right"
    fig.legend.orientation = "vertical"
    fig.legend.click_policy="hide"

    return fig



# bokeh piechart    
def bokeh_piechart(df, x='value', y='counts', figure=None, radius=0.8, title=''):
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
            source=df)
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


def bokeh_corr_plot(df, x='x_values', y='y_values',  figure=None, title='', markersize='markersize',  xlabel='Answers', ylabel='Number of answers', alpha=None):
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
    fig.circle(source=df, x=x, y=y, radius = 0.9)#size=markersize, fill_color={'field': 'region', 'transform': color_mapper}, fill_alpha=alpha)
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