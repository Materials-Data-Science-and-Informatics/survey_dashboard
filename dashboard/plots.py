
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure as bokeh_figure
from bokeh.palettes import Category20c
from bokeh.transform import factor_cmap
from bokeh.transform import cumsum
from bokeh.models import FactorRange


# for tests
#import pandas as pd
#import random
#from bokeh.io import output_notebook, show, push_notebook

#x = [str(i) for i in range(7)]
#xs = [x,x,x,x,x]
#xlabels = [[f'1 pli bla blub {i}' for i in x], [f'2 pli bla blub {i}' for i in x], [f'3 pli bla blub {i}' for i in x], [f'4 pli bla blub {i}' for i in x], [f'5 pli bla blub {i}' for i in x]]
#ys = [[random.randint(0, 1200) for i in x], [random.randint(0, 1200) for i in x], [random.randint(0, 1200) for i in x],[random.randint(0, 1200) for i in x], [random.randint(0, 1200) for i in x]]

# bokeh bar plot
def bokeh_barchart(df, x='value', y='counts', factors=None, figure=None, title='', width=0.9,  xlabel='Answers', ylabel='Number of answers', palette=Category20c, fill_color='color'):
    """Plot an interactive bar chart with bokeh"""
    
    if isinstance(df, ColumnDataSource):
        xdata = df.data[x]
        if not 'color' in df.column_names:
            if not len(xdata) > 20:
                df.data['color'] = Category20c[len(xdata)] # ! if len(xdata)>20 this fails
    else:
        xdata = df[x]
        if not 'color' in df.columns:
            df['color'] = Category20c[len(xdata)] # ! if len(xdata)>20 this fails

    if figure is None:
        if factors is not None:
            fig = bokeh_figure(plot_height=600, plot_width=600,
               title=title,
               toolbar_location='right',
               x_range=FactorRange(factors=factors),
               tools='',#'hover',
               tooltips=[('Data', f'@{x}'), ('Count', f'@{y}')])
        else:
            fig = bokeh_figure(plot_height=600, plot_width=600,
               title=title,
               toolbar_location='right',
               tools='',#'hover',
               tooltips=[('Data', f'@{x}'), ('Count', f'@{y}')])
    else:
        fig = figure
    #if factors is not None:
    #    fig.x_range=FactorRange(factors=factors)
    
    fig.vbar(x=x, top=y, width=width, source=df, line_color="white", fill_color=fill_color)#factor_cmap('x', palette=palette, factors=factors, start=1, end=2))
    fig.y_range.start = 0
    fig.x_range.range_padding = 0.1
    fig.xaxis.major_label_orientation = 1
    fig.xgrid.grid_line_color = None
    fig.yaxis.axis_label = ylabel
    fig.xaxis.axis_label = xlabel

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
        fig = bokeh_figure(plot_height=600, plot_width=600,
               title=title,
               toolbar_location='right',
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
            legend_field='xlabel',
            source=df)
    
    fig.axis.axis_label = None
    fig.axis.visible = False
    fig.grid.grid_line_color = None
    return fig

# test
#df_test = pd.DataFrame(data=dict(value=xs[0], counts=ys[0], xlabel=xs[0]))
#fig = bokeh_piechart(df_test)
#show(fig)