# myapp.py

import random

import os
from random import randint
from os.path import dirname, join

from bokeh.layouts import column, row
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import curdoc
from bokeh.models import ColumnDataSource, Div, Select
from bokeh.plotting import figure as bokeh_figure
from bokeh.models import CheckboxButtonGroup, CustomJS
from masci_tools.vis.bokeh_plots import bokeh_scatter, bokeh_multi_scatter
from .plots import bokeh_barchart, bokeh_piechart

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), sizing_mode="stretch_width")

pwd = os.getcwd()
questions = open(join(pwd, 'dashboard/data/questions.txt')).read().split('\n')
QUESTION_MAP = {question : i for i, question in enumerate(questions)}

question_select = Select(title="Question", value="Question 1",
               options=questions)
filter_select = Select(title="Data Filter", value="All",
               options=open(join(pwd, 'dashboard/data/filters.txt')).read().split('\n'))

#LABELS = open(join(pwd, 'dashboard/data/filters.txt')).read().split('\n')

#filter_select = CheckboxButtonGroup(labels=LABELS, active=[0, 1])
#filter_select.js_on_click(CustomJS(code="""
#    console.log('checkbox_button_group: active=' + this.active, this.toString())
#"""))
chart_select = Select(title="Chart type", value="bar",
               options=['bar', 'pie'])

# Controls 2
question_select2 = Select(title="Question X-Axis", value="Question 1",
               options=questions)
question_select3 = Select(title="Question Y-Axis", value="Question 2",
               options=questions)

TOOLTIPS=[
    ("Title", "@title"),
    ("Answer", "@x"),
    ("Number of Answers", "@y")
]


x = [str(i) for i in range(7)]
xs = [x,x,x,x,x]
#xs = [[f'1 pli bla blub {i}' for i in x], [f'2 pli bla blub {i}' for i in x], [f'3 pli bla blub {i}' for i in x], [f'4 pli bla blub {i}' for i in x], [f'5 pli bla blub {i}' for i in x]]
ys = [[randint(0, 1200) for i in x], [randint(0, 1200) for i in x], [randint(0, 1200) for i in x],[randint(0, 1200) for i in x], [randint(0, 1200) for i in x]]



#fig = bokeh_figure(height=600, width=700, title="", toolbar_location='right', tooltips=TOOLTIPS, sizing_mode="scale_both")
source = ColumnDataSource(data=dict(value=xs[0], counts=ys[0]))
source2 = ColumnDataSource(data=dict(value=xs[1], counts=ys[1]))

fig = bokeh_barchart(source, factors=xs[0])
fig2 = bokeh_barchart(source2, factors=xs[1])

#fig2 = bokeh_multi_scatter(source2, marker_size=[int(x)+6 for x in xs[1])


def select_data():
    """Select the data to display"""
    question = question_select.value
    index = QUESTION_MAP[question]
    selected = ColumnDataSource(data=dict(value=xs[index], counts=ys[index], factors=xs[index]))#, title=question))
    return selected

def select_data2():
    """Select the data to display"""
    question = question_select2.value
    question2 = question_select3.value
    index = QUESTION_MAP[question]
    selected = ColumnDataSource(data=dict(value=xs[index], counts=ys[index], factors=xs[index]))#, title=question))
    return selected



def select_chart():
    """Select how the data should be displayed"""
    charttype = chart_select.value.strip()
    return charttype

def update():
    """Update the charts"""
    df = select_data()
    charttype = select_chart()
    
    source.data = dict(value=df.data['value'], counts=df.data['counts'])
    
    if charttype == 'pie':
        fig = bokeh_piechart(source)#, figure=figure)
        row1.children[1] = fig
    else:
        fig = bokeh_barchart(source, factors=df.data['factors'])#, figure=figure)
        row1.children[1] = fig
    #show(fig)

def update2():
    """Update the charts"""
    df = select_data2()    
    source2.data = dict(value=df.data['value'], counts=df.data['counts'])
    fig2 = bokeh_barchart(source2, factors=df.data['factors'])

controls = [question_select, filter_select, chart_select]

inputs = column(*controls, width=200)
row1 = row(inputs, fig)
for control in controls:
    control.on_change('value', lambda attr, old, new: update())
first = column(desc, row1 , sizing_mode="scale_both")


controls2 = [question_select2, question_select3]
for control in controls2:
    control.on_change('value', lambda attr, old, new: update2())
inputs2 = column(*controls2, width=200)
layout = column(first, row(inputs2, fig2), sizing_mode="scale_both")

curdoc().add_root(layout)
curdoc().title = "HMC Survey Dashboard"