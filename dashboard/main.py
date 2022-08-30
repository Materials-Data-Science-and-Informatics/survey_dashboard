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
This file contains the main code for the dashboard and its layout.
"""
import random
import os
from random import randint
from os.path import dirname, join
import pandas as pd
#import panel as pn
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
from bokeh.client import logging
from masci_tools.vis.bokeh_plots import bokeh_scatter, bokeh_multi_scatter
from .plots import bokeh_barchart, bokeh_piechart, add_legend_at, bokeh_corr_plot#, bokeh_barchart2
from .plots import create_legend_corr
from .analysis import calculate_crosstab, prepare_data_research_field, filter_dataframe
from .analysis import percentage_to_area
from .data.helpers.hcs_clean_dictionaries import HCSquestions, HCS_orderedCats, HCS_MCsubquestions
from .data.helpers.hcs_clean_dictionaries import HCS_colnamesDict, abbrevCenterAffilDict


HCS_COLNAMES_REVERT_DICT = {val:key for key, val in HCS_colnamesDict.items()}
pwd = os.getcwd() # todo better use the absolute location of this file...
datafilepath= join(pwd, 'dashboard/data/20211130_HMCCommSurvey_clean.csv')


header = Div(text=open(join(dirname(__file__), "hmc_layout/header_.html")).read(), sizing_mode="stretch_width")
footer = Div(text=open(join(dirname(__file__), "hmc_layout/footer_.html")).read(), sizing_mode="stretch_width")

pwd = os.getcwd()
questions = open(join(pwd, 'dashboard/data/barchart_allowed.txt')).read().split('\n')
QUESTION_MAP = {question : i for i, question in enumerate(questions)}
FILTER_OPTIONS = open(join(pwd, 'dashboard/data/filters.txt')).read().split('\n')
MARGINS = (10,10,10,10)

# Data displayed on startup:
START_DATA_BAR = "careerLevel"
START_DATA_CORR_1 = "careerLevel"
START_DATA_CORR_2 = "docStructured"


# colors of research areas
#ra_colors = {'All': "#75968f", 'Chemistry': "#a5bab7", 'Earth Science':"#c9d9d3", 
#Engineering Science': "#e2e2e2", 'Life Science': "#dfccce", 'Mathematics': "#ddb7b1", 
#'Other': "#cc7878", 'Physics': "#933b41", 'Psychology': "#550b1d"}
re = ['All', 'Cum. Sum', 'Chemistry', 'Earth Science', 'Engineering Science', 'Life Science', 
      'Mathematics', 'Other', 'Physics', 'Psychology']
re_c = Category20c[len(re)]
ra_colors = {field: re_c[i] for i, field in enumerate(re)}


# Read data
survey_data = pd.read_csv(datafilepath)
source = ColumnDataSource(survey_data)
source_corr = ColumnDataSource(survey_data)


#### Control widgets

# Bar chart
# D: question select could also be a slider?
question_select = Select(title="Question", value=START_DATA_BAR,
    options=questions, description="Select the survey question, which results should be displayed.", margin=MARGINS)

multi_choice = MultiChoice(title="Filter data", value=["Cum. Sum", "Physics"], options=FILTER_OPTIONS, 
    description="Select which data subset to be displayed.", margin=MARGINS)

# D: better than a Select would be to use the HMC template for this...
# D: Maybe have two dashboards running a German and a English one and link build in the link in the template...
#lang_select = Select(title="Language", value="en",
#               options=['en', 'de'], description="Change the language of the Dashboard.")

# Correlation plot
question_select2 = Select(title="Question X-Axis", value=START_DATA_CORR_1,
               options=questions, description="Select the survey question which results should be displayed on the X-Axis.")
question_select3 = Select(title="Question Y-Axis", value=START_DATA_CORR_2,
               options=questions, description="Select the survey question which results should be displayed on the Y-Axis.")


# Others
plot_aspect_ratio_select = Select(title="Filter data", value="Cum. Sum",
               options=FILTER_OPTIONS)
menu = [('Barchart', 'bar_chart'), ('Correlation Plot', '(corr_plot')]
button_bar = Dropdown(label="Add a chart", button_type="success", menu=menu)
#button_corr = Button(label="Add correlation chart display", button_type="success")

TOOLTIPS=[
    ("Title", "@title"),
    ("Answer", "@x"),
    ("Number of Answers", "@y")
]



def select_data(question_select=question_select, multi_choice=multi_choice):
    """Select the data to display"""

    question = question_select.value
    q_index = question  #index = QUESTION_MAP[question]
    question_full = HCSquestions['EN'][HCS_COLNAMES_REVERT_DICT[question]]
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
    selected = ColumnDataSource(data=data)
    #dict(value=values, counts=counts, factors=values, color=colors, legend_labels=data_filters))#, title=question))
    ydata_spec = ColumnDataSource(data=ydata_spec)

    return selected, ydata_spec, question_full



def select_data_corr(question_select2=question_select2, question_select3=question_select3):
    """Select the data to display"""

    question = question_select2.value
    question2 = question_select3.value
    
    #q1_key = QUESTION_MAP[question]
    q1_key = question
    q2_key = question2

    # Enforced order of x and y axis 
    x_range = HCS_orderedCats[q1_key] #list(survey_data[q1_key].value_counts().keys())
    y_range = HCS_orderedCats[q2_key] #list(survey_data[q2_key].value_counts().keys())

    # If this is slow to calculate each time, it might make sense to calculate all of these 
    # at start up. i.e n^2 tables
    cross_tab = calculate_crosstab(survey_data, q1_key, q2_key)
    # marker size is radius, we want the Area to be proportional to the value
    # we also scale the markers with the max values are to small, or depending how many Cat, or 
    # figure width...
    marker_scale = 20.0
    cross_tab['markersize'] = percentage_to_area(cross_tab['percentage'], scale_m=marker_scale)
    cross_tab['x_values'] = cross_tab[q1_key]
    cross_tab['y_values'] = cross_tab[q2_key]
    cross_tab['color'] = ['#A0235A' for i in cross_tab[q2_key]]
    
    # for hover tool
    tooltips = [(f"{q1_key}", "@x_values"), 
                    (f"{q2_key}", "@y_values"),
                  ("total", "@total"),
                  ("percentage", "@percentage")]

    title = f'{q1_key} in dependence to {q2_key}'
    # Bokeh plots need a ColumnDataSource, but this can be initialized from a pandas
    #selected = ColumnDataSource(data=dict(x_values=cross_tab[q1_key], y_values=cross_tab[q2_key],
    #    markersize=cross_tab['percentage'], total=))

    selected = ColumnDataSource(cross_tab)

    display_options = {'x_range' : x_range, 'y_range' : y_range, 
                       'tooltips' : tooltips, 'title': title}
    return selected, display_options, marker_scale



#def select_chart(chart_select=chart_select):
##   """Select how the data should be displayed"""
#    chart_type = chart_select.value.strip()
#    return chart_type

def update(ob_index=0):
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
    fig = bokeh_barchart(source, y=y_keys, factors=y_keys, legend_labels=y_keys, fill_color=fill_colors, title=f'Q: {question}', orientation='vertical')#df.data['factors'], legend_labels='legend_labels')#, figure=figure)
    fig.margin = MARGINS
    #fig2 = bokeh_barchart(source, y=y_keys, factors=y_keys, legend_labels=y_keys, fill_color=fill_colors, title=question, orientation='horizontal')#'horizontal')#df.data['factors'], legend_labels='legend_labels')#, figure=figure)
    #fig2.margin = MARGINS

    tab1 = Panel(child=fig, title="Vertical Bar chart")
    tab2 = Panel(child=fig, title="Horizontal Bar chart")
    tab3 = Panel(child=fig, title="Pie chart")
    tabs = Tabs(tabs=[tab1, tab2, tab3])
    row2.children[ob_index] = tabs
    #add_legend_at(fig)

def update_corr(ob_index=1):
    """Update the correlation plot"""
    df, display_options, marker_scale = select_data_corr()    
    fig_corr = bokeh_corr_plot(df, **display_options)
    leg_corr = create_legend_corr(fig_corr, colors=df.data['color'], scale_m=marker_scale)
    #fig_corr.margin = MARGINS

    row3.children[ob_index] = fig_corr
    row3.children[ob_index+1] = leg_corr



# Generate Start figures

start_display_data, ydata_spec, question= select_data()
y_keys = ydata_spec.data['y_keys']
fill_colors = ydata_spec.data['colors']
fig = bokeh_barchart(start_display_data, y=y_keys, factors=y_keys, legend_labels=y_keys, 
    fill_color=fill_colors, title=f'Q: {question}', orientation='vertical')#factors=start_display_data.data['factors'])

#fig.margin = MARGINS
start_corr_data, display_options, marker_scale = select_data_corr()
fig_corr = bokeh_corr_plot(start_corr_data, **display_options)
leg_corr = create_legend_corr(fig_corr, colors=start_corr_data.data['color'], scale_m=marker_scale)
#fig_corr.margin = MARGINS
#fig2 = bokeh_barchart(source_corr)

#fig2 = bokeh_multi_scatter(source2, marker_size=[int(x)+6 for x in xs[1])


def generate_bar_controls():
    controls_bar = [question_select, multi_choice]
    return controls_bar

def generate_corr_controls():
    controls_corr = [question_select2, question_select3]
    return controls_corr



# Dashboard layout

# for spaces: https://docs.bokeh.org/en/latest/docs/reference/models/layouts.html#spacer
controls_bar = generate_bar_controls()
inputs = column(*controls_bar, width=800)
for control in controls_bar:
    control.on_change('value', lambda attr, old, new: update())

controls_corr = generate_corr_controls()
for control in controls_corr:
    control.on_change('value', lambda attr, old, new: update_corr())
inputs_corr = column(*controls_corr, width=200)

# create tabs
tab1 = Panel(child=fig, title="Vertical Bar chart")
tab2 = Panel(child=fig, title="Horizontal Bar chart")
tab3 = Panel(child=fig, title="Pie chart")
tabs = Tabs(tabs=[tab1, tab2, tab3])

row1 = row(inputs)
row2 =  row(tabs)
row3 = row(inputs_corr, fig_corr, leg_corr)
first = column(header, row1, sizing_mode="scale_both")
layout = column(first, row2, row3, row(button_bar), footer, sizing_mode="scale_both")

#row1 = pn.Row(inputs, tabs, fig_corr, inputs_corr)
#first = pn.Column(desc, row1, sizing_mode="scale_both")
#layout = pn.Ccolumn(first, pn.Row(button_bar), sizing_mode="scale_both")


curdoc().add_root(layout)
curdoc().title = "HMC Survey Dashboard"