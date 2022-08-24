# myapp.py

import random

import os
from random import randint
from os.path import dirname, join
import pandas as pd
from bokeh.models import Panel, Tabs
from bokeh.layouts import column, row
from bokeh.models import Dropdown
from bokeh.palettes import RdYlBu3
from bokeh.palettes import Category20c

from bokeh.plotting import curdoc
from bokeh.models import ColumnDataSource, Div, Select
from bokeh.plotting import figure as bokeh_figure
from bokeh.models import CheckboxButtonGroup, CustomJS
from bokeh.models import MultiChoice
from bokeh.models import Paragraph
from masci_tools.vis.bokeh_plots import bokeh_scatter, bokeh_multi_scatter
from .plots import bokeh_barchart, bokeh_piechart, add_legend_outside, bokeh_corr_plot#, bokeh_barchart2
from .analysis import calculate_crosstab, prepare_data_research_field, filter_dataframe


pwd = os.getcwd() # todo better use the absolute location of this file...
datafilepath= join(pwd, 'dashboard/data/20211130_HMCCommSurvey_clean.csv')

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), sizing_mode="stretch_width")

pwd = os.getcwd()
questions = open(join(pwd, 'dashboard/data/barchart_allowed.txt')).read().split('\n')
QUESTION_MAP = {question : i for i, question in enumerate(questions)}
FILTER_OPTIONS = open(join(pwd, 'dashboard/data/filters.txt')).read().split('\n')

# question select could also be a slider?
question_select = Select(title="Question", value="careerLevel",
               options=questions)
filter_select = Select(title="Filter data", value="All",
               options=FILTER_OPTIONS)

multi_choice = MultiChoice(title="Filter data", value=["All", "Physics"], options=FILTER_OPTIONS)
multi_choice.js_on_change("value", CustomJS(code="""
    console.log('multi_choice: value=' + this.value, this.toString())
"""))

#LABELS = open(join(pwd, 'dashboard/data/filters.txt')).read().split('\n')

#chart_select = Select(title="Chart type", value="bar",
#               options=['bar', 'pie'], description="Plot the same Data as Piechart")

lang_select = Select(title="Language", value="en",
               options=['en', 'de'], description="Change the language of the Dashboard.")

# Controls 2
question_select2 = Select(title="Question X-Axis", value="careerLevel",
               options=questions, description="Select the question which results should be displayed on the X-Axis.")
question_select3 = Select(title="Question Y-Axis", value="docStructured",
               options=questions, description="Select the question which results should be displayed on the Y-Axis.")

menu = ['Barchart, Diffchart, Correlation Plot']
button_bar = Dropdown(label="Add a chart", button_type="success", menu=menu)
#button_corr = Button(label="Add correlation chart display", button_type="success")

TOOLTIPS=[
    ("Title", "@title"),
    ("Answer", "@x"),
    ("Number of Answers", "@y")
]

# colors of research areas
#ra_colors = {'All': "#75968f", 'Chemistry': "#a5bab7", 'Earth Science':"#c9d9d3", 'Engineering Science': "#e2e2e2", 'Life Science': "#dfccce", 'Mathematics': "#ddb7b1", 'Other': "#cc7878", 'Physics': "#933b41", 'Psychology': "#550b1d"}
re = ['All', 'Chemistry', 'Earth Science', 'Engineering Science', 'Life Science', 'Mathematics', 'Other', 'Physics', 'Psychology']
re_c = Category20c[len(re)]
ra_colors = {field: re_c[i] for i, field in enumerate(re)}
#x = [str(i) for i in range(7)]
#xs = [x,x,x,x,x]
#xs = [[f'1 pli bla blub {i}' for i in x], [f'2 pli bla blub {i}' for i in x], [f'3 pli bla blub {i}' for i in x], [f'4 pli bla blub {i}' for i in x], [f'5 pli bla blub {i}' for i in x]]
#ys = [[randint(0, 1200) for i in x], [randint(0, 1200) for i in x], [randint(0, 1200) for i in x],[randint(0, 1200) for i in x], [randint(0, 1200) for i in x]]
#counts2 = sum(zip(*ys), ())
#factors = [(str(ques), ans) for ques in range(len(xs)) for ans in xs[0]] # factors have to be unique, and strings
#df_test3 = ColumnDataSource(data=dict(value=factors, counts=counts2))

survey_data = pd.read_csv(datafilepath)

#fig = bokeh_figure(height=600, width=700, title="", toolbar_location='right', tooltips=TOOLTIPS, sizing_mode="scale_both")
source = ColumnDataSource(survey_data)
source_corr = ColumnDataSource(survey_data)

def select_data(question_select=question_select, multi_choice=multi_choice):
    """Select the data to display"""

    question = question_select.value
    #index = QUESTION_MAP[question]
    q_index = question
    to_exclude = []
    #TODO map the question to index/key
    #TODO there should be a certain display order, i.e mappings needed
    #TODO, also some things are excluded

    data_filters = multi_choice.value

    # need something like [index: index_name, full question: '', title; '', 'key order' : [], 'skipped keys':[]]
    
    # for now this is greedy, if to slow think of another way
    # we want to display anything in terms of researchArea, todo better was to d filter, generalize this
    df = filter_dataframe(survey_data, include=[q_index, "researchArea"], exclude=[(q_index, to_exclude)])
    
    exclude = []
    for field in re:
        if field not in data_filters:
            exclude.append(field)
    for area in exclude:
        df = df[df["researchArea"] != area]
    data, y_keys = prepare_data_research_field(df, q_index)
    #df = pd.DataFrame.from_dict(data)


    #data_filters = y_keys
    ydata_spec = {}
    colors = []
    for key in y_keys:
        if key in data_filters:
            colors.append(ra_colors[key])
    
    ydata_spec['y_keys'] = data_filters
    ydata_spec['colors'] = colors
    ydata_spec['legend_labels'] = data_filters
    selected = ColumnDataSource(data=data)#dict(value=values, counts=counts, factors=values, color=colors, legend_labels=data_filters))#, title=question))
    ydata_spec = ColumnDataSource(data=ydata_spec)
    return selected, ydata_spec, question



def select_data_corr(question_select2=question_select2, question_select3=question_select3):
    """Select the data to display"""
    question = question_select2.value
    question2 = question_select3.value
    
    #q1_key = QUESTION_MAP[question]
    q1_key = question
    q2_key = question2
    
    # If this is slow to calculate each time, it might make sense to calculate all of these from the at start up.
    # i.e n^2 tables
    cross_tab = calculate_crosstab(survey_data, q1_key, q2_key) 
    print(cross_tab.keys())
    #totals = survey_data[question].value_counts()
    counts = cross_tab['percentage']
    values = cross_tab['percentage']#cross_tab['total']
    # Bokeh plots need a ColumnDataSource, but this can be initialized from a pandas
    selected = ColumnDataSource(data=dict(x_values=values, y_values=values, counts=counts))#, title=question))
    return selected



#def select_chart(chart_select=chart_select):
##   """Select how the data should be displayed"""
#    chart_type = chart_select.value.strip()
#    return chart_type

def update():
    """Update the charts"""
    df, ydata_spec, question = select_data()
    #charttype = select_chart(chart_select=chart_select)
    
    #source.data = dict(value=df.data['value'], counts=df.data['counts'], legend_labels=df.data['legend_labels'])
    source = df
    # TODO: always plot piechart in seperate tab
    #if charttype == 'pie':
    #    fig = bokeh_piechart(source)#, figure=figure)
    #    row1.children[1] = fig
    #else:
        #print(y_keys, df.data['colors'])
    y_keys = ydata_spec.data['y_keys']
    fill_colors = ydata_spec.data['colors']
    fig = bokeh_barchart(source, y=y_keys, factors=y_keys, fill_color=fill_colors, title=question)#df.data['factors'], legend_labels='legend_labels')#, figure=figure)
    row1.children[1] = fig
    #add_legend_outside(fig)

def update_corr():
    """Update the charts"""
    df = select_data_corr()    
    fig_corr = bokeh_corr_plot(df)
    row1.children[2] = fig_corr


start_display_data, ydata_spec, question= select_data()
y_keys = ydata_spec.data['y_keys']
fill_colors = ydata_spec.data['colors']
fig = bokeh_barchart(start_display_data, y=y_keys, factors=y_keys, legend_labels=y_keys, fill_color=fill_colors, title=question)#factors=start_display_data.data['factors'])

start_corr_data = select_data_corr()
fig_corr = bokeh_corr_plot(start_corr_data)
#fig2 = bokeh_barchart(source_corr)

#fig2 = bokeh_multi_scatter(source2, marker_size=[int(x)+6 for x in xs[1])


def generate_bar_controls():
    controls_bar = [question_select, multi_choice]
    return controls_bar

def generate_corr_controls():
    controls_corr = [question_select2, question_select3]
    return controls_corr

# Dashboard layout
controls_bar = generate_bar_controls()
inputs = column(*controls_bar, width=200)
for control in controls_bar:
    control.on_change('value', lambda attr, old, new: update())

controls_corr = generate_corr_controls()
for control in controls_corr:
    control.on_change('value', lambda attr, old, new: update_corr())
inputs_corr = column(*controls_corr, width=200)


row1 = row(inputs, fig, fig_corr, inputs_corr)
first = column(desc, row1, sizing_mode="scale_both")
layout = column(first, row(button_bar), sizing_mode="scale_both")

curdoc().add_root(layout)
curdoc().title = "HMC Survey Dashboard"