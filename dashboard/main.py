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
#from bokeh.models import Panel, Tabs
import panel as pn
#from bokeh.layouts import column, row
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
#from masci_tools.vis.bokeh_plots import bokeh_scatter, bokeh_multi_scatter
from .plots import bokeh_barchart, bokeh_piechart, add_legend_at, bokeh_corr_plot#, bokeh_barchart2
from .plots import create_legend_corr, generate_wordcloud
from .analysis import calculate_crosstab, prepare_data_research_field, filter_dataframe
from .analysis import percentage_to_area, get_all_values
from .data.display_specifications.hcs_clean_dictionaries import HCSquestions, HCS_orderedCats, HCS_MCsubquestions
from .data.display_specifications.hcs_clean_dictionaries import HCS_colnamesDict, abbrevCenterAffilDict, HCS_MCList
from .data.display_specifications.hcs_clean_dictionaries import HCS_dtypesWOmc

HCS_COLNAMES_REVERT_DICT = {val:key for key, val in HCS_colnamesDict.items()}
HCSquestions_revert = {}
HCSquestions_revert['EN'] = {val:key for key, val in HCSquestions['EN'].items()}
HCSquestions_revert['DE'] = {val:key for key, val in HCSquestions['DE'].items()}

def map_qkey_to_question(key, lang='EN'):
    return HCSquestions[lang][HCS_COLNAMES_REVERT_DICT[key]]

def map_question_to_qkey(question, lang='EN'):
    return HCS_colnamesDict[HCSquestions_revert[lang][question]]

# create tabs
def construct_tabs(tab_list):
    return pn.Tabs(*tab_list, dynamic=True)

pwd = os.getcwd() # todo better use the absolute location of this file...
datafilepath= join(pwd, 'dashboard/data/hmc_survey_2021_data_cleaned.csv')
if not os.path.exists(datafilepath):
    from .data.download_data import download_data
    download_data()
desc = Div(text=open(join(dirname(__file__), "description.html")).read(), sizing_mode="stretch_width")
pwd = os.getcwd()
questions_keys = open(join(pwd, 'dashboard/data/display_specifications/barchart_allowed.txt')).read().split('\n')
questions = [map_qkey_to_question(key) for key in questions_keys]
#QUESTION_MAP = {question : i for i, question in enumerate(questions)}
FILTER_OPTIONS = open(join(pwd, 'dashboard/data/display_specifications/filters.txt')).read().split('\n')
FILTER_OPTIONS_METHOD = open(join(pwd, 'dashboard/data/display_specifications/filters_methods.txt')).read().split('\n')

# Data displayed on startup:
START_DATA_BAR = map_qkey_to_question("careerLevel")
START_DATA_CORR_1 = map_qkey_to_question("careerLevel")
START_DATA_CORR_2 = map_qkey_to_question("docStructured")


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
print(survey_data.columns)
# Rename columns to something more human Readable:
survey_data.rename(columns=HCS_colnamesDict, inplace=True)
print(survey_data.columns)
source = ColumnDataSource(survey_data)
source_corr = ColumnDataSource(survey_data)


#### Control widgets
# Bar chart
# D: question select could also be a slider?
question_select = pn.widgets.Select(name="Select a Question from the survey", value=START_DATA_BAR,
    options=questions)#, description="Select the survey question, which results should be displayed.")

multi_choice = pn.widgets.MultiChoice(name="Filter by research field", value=["All"], options=FILTER_OPTIONS)#, 
    #description="Select which data subset to be displayed.")
multi_choice_method = pn.widgets.MultiChoice(name="Filter by data generation method", value=[], options=FILTER_OPTIONS_METHOD)


# D: better than a Select would be to use the HMC template for this...
# D: Maybe have two dashboards running a German and a English one and link build in the link in the template...
#lang_select = Select(title="Language", value="en",
#               options=['en', 'de'], description="Change the language of the Dashboard.")

# Correlation plot
question_select2 = pn.widgets.Select(name="Question X-Axis", value=START_DATA_CORR_1,
               options=questions)#, description="Select the survey question which results should be displayed on the X-Axis.")
question_select3 = pn.widgets.Select(name="Question Y-Axis", value=START_DATA_CORR_2,
               options=questions)#, description="Select the survey question which results should be displayed on the Y-Axis.")


# Others
plot_aspect_ratio_select = pn.widgets.Select(name="Filter data", value="Cum. Sum",
               options=FILTER_OPTIONS)
menu = ['Barchart', 'Correlation Plot']#('Barchart', 'bar_chart'), ('Correlation Plot', '(corr_plot')]
button_bar = pn.widgets.Select(name="Add a chart", options=menu)

TOOLTIPS=[
    ("Title", "@title"),
    ("Answer", "@x"),
    ("Number of Answers", "@y")
]



def select_data():#question_select=question_select, multi_choice=multi_choice):
    """Select the data to display"""

    question = question_select.value
    q_index = map_question_to_qkey(question)
    question_full = question
    to_exclude = []
    #TODO there should be a certain display order, i.e mappings needed
    #TODO, also some things are excluded

    # Enforced order of x and y axis
    print(q_index)
    xtype = HCS_dtypesWOmc[q_index]
    if xtype == 'category':
        x_range = HCS_orderedCats[q_index]
        width = 0.1
    else:
        x_range = None
        width = 0.6
    
    data_filters = multi_choice.value
    data_filters_method = multi_choice_method.value
    method_include = []
    method_exclude = []
    methods_dict = HCS_MCsubquestions['dataGenMethod_']
    for method in data_filters_method:
        for key, val in methods_dict.items():
            if val == method:
                method_include.append(key)
                # Filter out the one who provided False
                method_exclude.append((key, [False]))
    
    # for now this is greedy, if to slow think of another way
    # we want to display anything in terms of researchArea, todo better was to d filter, generalize this
    df = filter_dataframe(survey_data, include=list(set([q_index, "researchArea"]+ method_include)), exclude=[(q_index, to_exclude)]+method_exclude)
    #df = filter_dataframe(df, include=[q_index, "researchArea"],  exclude=[(q_index, to_exclude)])
    data_all = get_all_values(df, q_index)

    exclude = []
    for field in re:
        if field not in data_filters:
            exclude.append(field)
    for area in exclude:
        df = df[df["researchArea"] != area]
    data, y_keys = prepare_data_research_field(df, q_index)
    if 'All' in data_filters:
        data['All'] = data_all['All']
    
    #data_filters = y_keys
    ydata_spec = {}
    colors = []
    for key in data_filters:
        colors.append(ra_colors[key])
    
    ydata_spec['y_keys'] = data_filters
    ydata_spec['colors'] = colors
    ydata_spec['legend_labels'] = data_filters
    selected = ColumnDataSource(data=data)
    ydata_spec = ColumnDataSource(data=ydata_spec)

    display_options = {'x_range' : x_range,
                       'title': f'Q: {question_full}', 'width': width}
    return selected, ydata_spec, display_options



def select_data_corr():#question_select2=question_select2, question_select3=question_select3):
    """Select the data to display"""

    question = question_select2.value
    question2 = question_select3.value
    
    #q1_key = QUESTION_MAP[question]
    q1_key = map_question_to_qkey(question)
    q2_key = map_question_to_qkey(question2)

    # Enforced order of x and y axis 
    xtype = HCS_dtypesWOmc[q1_key]
    if xtype == 'category':
        x_range = HCS_orderedCats[q1_key]
    else:
        x_range = None

    ytype = HCS_dtypesWOmc[q2_key]
    if ytype == 'category':
        y_range = HCS_orderedCats[q2_key]
    else:
        y_range = None


    data_filters = multi_choice.value
    data_filters_method = multi_choice_method.value
    
    method_include = []
    method_exclude = []
    methods_dict = HCS_MCsubquestions['dataGenMethod_']
    for method in data_filters_method:
        for key, val in methods_dict.items():
            if val == method:
                method_include.append(key)
                # Filter out the one who provided False
                method_exclude.append((key, [False]))

    exclude_area = []
    for field in re:
        if field not in data_filters:
            pass
            #exclude_area.append(("researchArea", [field]))
    #exclude_areas = ["researchArea", exclude_area]

    # If this is slow to calculate each time, it might make sense to calculate all of these 
    # at start up. i.e n^2 tables
    df = filter_dataframe(survey_data, include=list(set([q1_key, q2_key, "researchArea"] + method_include)), exclude=[]+method_exclude+exclude_area)

    cross_tab = calculate_crosstab(df, q1_key, q2_key)
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
    selected = ColumnDataSource(cross_tab)

    display_options = {'x_range' : x_range, 'y_range' : y_range, 
                       'tooltips' : tooltips, 'title': title}
    return selected, display_options, marker_scale

def select_data_wordcloud():
    """
    Filter data for wordcloud from data filters
    """
    word_list = []
    data_filters = multi_choice.value
    data_filters_method = multi_choice_method.value

    method_include = []
    method_exclude = []
    methods_dict = HCS_MCsubquestions['dataGenMethod_']
    method_keys = list(methods_dict.keys())
    for method in data_filters_method:
        for key in method_keys:
            if methods_dict[key] == method:
                method_include.append(key)
                # Filter out the one who provided False
                method_exclude.append((key, [False]))

    if len(data_filters_method) == 0:
        method_include = method_keys
        method_exclude = []


    data_get_methods_spec = []
    for method in method_include:
        id_meth = method[-1]
        data_get_methods_spec.append('dataGenMethodSpec_{}_1'.format(id_meth))
        data_get_methods_spec.append('dataGenMethodSpec_{}_2'.format(id_meth))
        data_get_methods_spec.append('dataGenMethodSpec_{}_3'.format(id_meth))
    
    df = filter_dataframe(survey_data, include=["researchArea"]+method_include+data_get_methods_spec, exclude=method_exclude, as_type ='str')
    exclude = []
    for field in re:
        if field not in data_filters:
            exclude.append(field)
    if 'All' in data_filters:
        exclude = []
    for area in exclude:
        df = df[df["researchArea"] != area]
    
    # prepare word list
    word_list = []
    for method in data_get_methods_spec:
        #print(df[method])
        w_list = [word for word in df[method] if str(word)!='nan']
        word_list = word_list + w_list #ent.replace(' ', '-') # Add '-'
        
    
    return word_list

def update(target, event, charttype=1):
    """Update the charts
    
    The target will be replaced, the event contains what interaction was trickered.
    Here we assume value change, because no others where allowed.
    """
    print(event)
    df, ydata_spec, display_options = select_data()
    source = df

    y_keys = ydata_spec.data['y_keys']
    fill_colors = ydata_spec.data['colors']
    fig = bokeh_barchart(source, y=y_keys, factors=y_keys, legend_labels=y_keys, fill_color=fill_colors, orientation='vertical', **display_options)#df.data['factors'], legend_labels='legend_labels')#, figure=figure)
    #fig2 = bokeh_barchart(source, y=y_keys, factors=y_keys, legend_labels=y_keys, fill_color=fill_colors, title=question, orientation='horizontal')#'horizontal')#df.data['factors'], legend_labels='legend_labels')#, figure=figure)

    #tab1 = ("Vertical Bar chart", pn.pane.Bokeh(fig))
    #tab2 = ("Horizontal Bar chart", pn.pane.Bokeh(fig))
    #tab3 = ("Pie chart", pn.pane.Bokeh(fig))
    #tabs = construct_tabs([tab1, tab2, tab3])
    #target.object = tabs#pn.pane.Bokeh(fig_corr)
    
    target.object = fig
    
    #row2.objects[ob_index] = tabs


def update_corr(target, event):
    """Update the correlation plot"""

    print(event)
    ob_index=1
    df, display_options, marker_scale = select_data_corr()
    fig_corr = bokeh_corr_plot(df, **display_options)
    leg_corr = create_legend_corr(fig_corr, colors=df.data['color'], scale_m=marker_scale)

    target.object = fig_corr


def update_wordcloud(target, event):
    """Update the correlation plot"""

    print(event)
    text_list = select_data_wordcloud()
    wordcloud = generate_wordcloud(text_list, height=800, width=1200)
    target.object =  wordcloud.to_svg()


# Generate Start figures

start_display_data, ydata_spec, display_options= select_data()
y_keys = ydata_spec.data['y_keys']
fill_colors = ydata_spec.data['colors']
fig = pn.pane.Bokeh(bokeh_barchart(start_display_data, y=y_keys, factors=y_keys, legend_labels=y_keys, 
    fill_color=fill_colors, orientation='vertical', **display_options))#factors=start_display_data.data['factors'])
fig2 = pn.pane.Bokeh(bokeh_barchart(start_display_data, y=y_keys, factors=y_keys, legend_labels=y_keys, 
    fill_color=fill_colors, orientation='vertical', **display_options))#factors=start_display_data.data['factors'])
fig3 = pn.pane.Bokeh(bokeh_barchart(start_display_data, y=y_keys, factors=y_keys, legend_labels=y_keys, 
    fill_color=fill_colors, orientation='vertical', **display_options))#factors=start_display_data.data['factors'])

start_corr_data, display_options, marker_scale = select_data_corr()
fig_corr_1 = bokeh_corr_plot(start_corr_data, **display_options)
fig_corr = pn.pane.Bokeh(fig_corr_1)
leg_corr = pn.pane.Bokeh(create_legend_corr(fig_corr_1, colors=start_corr_data.data['color'], scale_m=marker_scale))

# Wordcloud of tools
text_list = select_data_wordcloud()
wordcloud = generate_wordcloud(text_list, height=800, width=1200)
svg_pane = pn.pane.SVG(wordcloud.to_svg(), width=wordcloud.width, height=wordcloud.height)

def generate_bar_controls():
    controls_bar = [question_select, multi_choice, multi_choice_method]
    return controls_bar

def generate_corr_controls():
    controls_corr = [question_select2, question_select3]
    return controls_corr

md_text_global_filter = ("# Global data filters\n Select some data filters to apply. "
                         "You can filter by research area and or by data generation method.")

md_text_barchart = ("# Overview\n Use this area to explorer the results for each survey question. "
                    "Use the dropdown menus to select the question of interest.")

md_text_corrchart = ("# Basic Correlations\n Find out about basic correlation of answers, "
                    "i.e. how many participants provided the same answer two questions.")

md_text_button = ("# Further charts\n")

md_text_tools_used = ("# Tools and Methods\n Find out about the tools and methods used in the "
                    "research area and data generation method you filtered for.")

####################
# Dashboard layout #
####################

controls_bar = generate_bar_controls()
for control in controls_bar:
    #control.param.watch(update, ['value'], onlychanged=True)
    control.link(fig, callbacks={'value': update})
    #control.link(fig2, callbacks={'value': update})
    #control.link(fig3, callbacks={'value': update})
    #control.link(tabs, callbacks={'value': update})
    control.link(svg_pane, callbacks={'value': update_wordcloud})
    #control.link(svg_pane, callbacks={'value': update_corr})

tab1 = ("Vertical Bar chart", fig)
tab2 = ("Horizontal Bar chart", fig2)
tab3 = ("Pie chart", fig3)
tabs = construct_tabs([tab1, tab2, tab3])

controls_corr = generate_corr_controls()
for control in controls_corr:
    control.link(fig_corr, callbacks={'value': update_corr})

# Layout with Panel
# We provide the layout in this explicit way and not all in one list because first we addresed the objects
# over the rows name, now this may be obsolete

inputs = pn.Column(*controls_bar, width=800)
inputs_corr = pn.Column(*controls_corr, width=800)

row1 = pn.Column(desc, md_text_global_filter, pn.Row(inputs), sizing_mode="scale_both")
row2 =  pn.Row(tabs)
row3 = pn.Column(inputs_corr, pn.Row(fig_corr, leg_corr))
row5 = pn.Row(button_bar)
row4 = pn.Column(md_text_tools_used, svg_pane)
layout = pn.Column(row1, md_text_barchart, row2, md_text_corrchart, row3, row4, sizing_mode="scale_both", title='HMC Survey Dashboard')
#md_text_button, row4, sizing_mode="scale_both", title='HMC Survey Dashboard')

layout.servable(title='HMC Survey Dashboard')