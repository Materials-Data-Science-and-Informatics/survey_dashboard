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
import os
from os.path import dirname, join
import pandas as pd
import panel as pn
from bokeh.palettes import Category20
from bokeh.models import ColumnDataSource, Div
from .plots import bokeh_barchart, bokeh_piechart, add_legend_at, bokeh_corr_plot
from .plots import create_legend_corr, generate_wordcloud, interactive_wordcloud
from .plots import DEFAULT_FIGURE_WIDTH, DEFAULT_FIGURE_HEIGHT
from .analysis import calculate_crosstab, prepare_data_research_field, filter_dataframe
from .analysis import percentage_to_area, get_all_values
from .data.display_specifications.hcs_clean_dictionaries import HCSquestions, HCS_orderedCats, HCS_MCsubquestions
from .data.display_specifications.hcs_clean_dictionaries import HCS_colnamesDict, abbrevCenterAffilDict, HCS_MCList
from .data.display_specifications.hcs_clean_dictionaries import HCS_dtypesWOmc, HCS_MCList, HCS_MCsubquestions
from .text_display import *
from .data.display_specifications.hcs_clean_dictionaries import FILTER_OPTIONS, BARCHART_ALLOWED
from .data.display_specifications.hmc_custom_layout import hmc_custom_css_accordion


# GLOBAL
LANGUAGE = os.environ.get('LANGUAGE_DASHBOARD', 'EN') #'DE'
ACCORDION_WIDTH = int(DEFAULT_FIGURE_WIDTH*2) # maybe this can be made dynamic. 
# This is the only width parameter to which everything streches to 

pn.config.loading_spinner = 'dots'
pn.config.loading_color = '#005AA0'
pn.config.raw_css = [hmc_custom_css_accordion]

# Specific data configuration for the HMC survey data
HCS_COLNAMES_REVERT_DICT = {val:key for key, val in HCS_colnamesDict.items()}
HCSquestions_revert = {}
HCSquestions_revert[LANGUAGE] = {val:key for key, val in HCSquestions[LANGUAGE].items()}
HCS_MCsubquestions_flattened = {}
for key, val in HCS_MCsubquestions.items():
    for ke, va in val.items():
        HCS_MCsubquestions_flattened[ke] = va

# if LANGUAGE = 'DE', we translate the data entries because these will often be used as tick labels


# Small Helpers functions 

def map_qkey_to_question(key: str, lang:str =LANGUAGE)-> str:
    """
    Given a key return the full question to be displayed associated with the key for a given language
    """
    mc_key = key

    if key in HCS_MCList:
        # Multiple choice, all have the same question for now
        mc_key = list(HCS_MCsubquestions[key].keys())[0]
        #print(mc_key)
        index = HCS_COLNAMES_REVERT_DICT[mc_key].split('/')[0]
        #print(index)
    else:
        index = HCS_COLNAMES_REVERT_DICT[mc_key]

    return HCSquestions[lang][index]

def map_question_to_qkey(question: str, lang:str =LANGUAGE) -> list:
    """
    Map a given question String to the corresponding columns keys in the dataframe

    usually this is one column, but for multiple choice this can be several columns.
    """
    column_keys = []
    key = HCSquestions_revert[lang][question]
    if key in HCS_MCList:
        print(f'Multiple Choice,{key}')
        #for multiple choice this is a list of subquestions
        key_s = key + '/'
        for key in HCS_colnamesDict.keys():
            if key_s in key:
                if not 'other' in key: # for now, needs to be included in HCS_MCsubquestions and others is strange
                    column_keys.append(HCS_colnamesDict[key])
        column_keys.sort() # Wrong sort... _1 _10 _2 ...
    else:
        column_keys.append(HCS_colnamesDict[key])
    return column_keys

# create tabs
def construct_tabs(tab_list):
    return pn.Tabs(*tab_list)#, dynamic=True)

pwd = os.getcwd() # TODO better use the absolute location of the main.py file...
datafilepath= join(pwd, 'survey_dashboard/data/hmc_survey_2021_data_cleaned.csv')
if not os.path.exists(datafilepath):
    from .data.download_data import download_data
    print('Downloading Data')
    download_data()

# For the dashboard presentation, we load some metadata to certain stuff out of the HMC graph.
# However this gets prepared in before in as a new dataframe

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), sizing_mode="stretch_width")
pwd = os.getcwd()
questions_keys = BARCHART_ALLOWED
questions = [map_qkey_to_question(key) for key in questions_keys]

# Data displayed on startup:

# Overview
# TODO combine plots to something nice, high information density
START_DATA_OV1 = map_qkey_to_question("fairFamiliarity") #and ocid and docStructured
START_DATA_OV2 = map_qkey_to_question("yearsInResearch")
START_DATA_OV3 = map_qkey_to_question("researchArea")
START_DATA_OV4 = map_qkey_to_question("pubAmount")

# Methods:
# Software tools, wordclouds, data generation methods

# Questions explorer
START_DATA_BAR = map_qkey_to_question("careerLevel")
START_DATA_BAR2 = map_qkey_to_question("docStructured")
START_DATA_CORR_1 = map_qkey_to_question("careerLevel")
START_DATA_CORR_2 = map_qkey_to_question("docStructured")

FILTER_BY = "researchArea"
FILTER_BY_2 = "dataGenMethod_"

TOOLTIPS=[
    ("Title", "@title"),
    ("Answer", "@x"),
    ("Number of Answers", "@y")
]


# colors of research areas
#ra_colors = {'All': "#75968f", 'Chemistry': "#a5bab7", 'Earth Science':"#c9d9d3", 
#Engineering Science': "#e2e2e2", 'Life Science': "#dfccce", 'Mathematics': "#ddb7b1", 
#'Other': "#cc7878", 'Physics': "#933b41", 'Psychology': "#550b1d"}
re_fields = ['All', 'Cum. Sum', 'Chemistry', 'Earth Science', 'Engineering Science', 'Life Science', 
      'Mathematics', 'Other', 'Physics', 'Psychology', 'Other']
re_c = Category20[len(re_fields)]
ra_colors = {field: re_c[i] for i, field in enumerate(re_fields)}


# Read data
survey_data = pd.read_csv(datafilepath)

# Rename columns to something more human Readable: #TODO stay with orginal
survey_data.rename(columns=HCS_colnamesDict, inplace=True)

# Different sources, because there wil be different filters applied to these.
source = ColumnDataSource(survey_data)
source_corr = ColumnDataSource(survey_data)


def select_data(question, data_filters, data_filters_method, filter_by=FILTER_BY):
    """Select the data to display"""
    print(question)
    q_index = map_question_to_qkey(question)
    print(q_index)
    q_index_0 = q_index[0]
    question_full = question
    to_exclude = []

    # due to data cleaning some columns are removed...
    # we ignore them if they are not in the index.... to avoid KeyErrors
    q_index_clean = []
    keys = list(survey_data.keys())
    for key in q_index:
        if key in keys:
            q_index_clean.append(key)

    exclude_nan = True
    if len(q_index) >1:
        exclude_nan = False

    method_include = []
    method_exclude = []
    methods_dict = HCS_MCsubquestions[FILTER_BY_2]
    for method in data_filters_method:
        for key, val in methods_dict.items():
            if val == method:
                method_include.append(key)
                # Cut out the rows out the ones who provided False
                method_exclude.append((key, [False]))
    #print(list(set([FILTER_BY]+ q_index_clean + method_include)))
    #print(method_exclude)


    include_clean = list(set([FILTER_BY]+ q_index_clean + method_include))
    # for now this is greedy, if too slow think of another way
    # we want to display anything in terms of researchArea, todo better was to filter, generalize this
    df = filter_dataframe(survey_data, include=include_clean, exclude=method_exclude, exclude_nan=exclude_nan)# [(q_index, to_exclude)]+
    data_all = get_all_values(df, q_index_clean, display_dict=HCS_MCsubquestions_flattened)

    exclude = []
    for field in re_fields:
        if field not in data_filters:
            exclude.append(field)
    for filter_key in exclude:
        df = df[df[filter_by] != filter_key]
    data, y_keys = prepare_data_research_field(df, q_index) # this add also Cum. Sum.
    if 'All' in data_filters:
        data['All'] = data_all['All']
    #print(data)
    # We create two ColumnDataSources, because they have to be n*n and 
    # it is therefore not posible to put all specifics into one 
    ydata_spec = {}
    colors = []
    for key in data_filters:
        colors.append(ra_colors[key])

    # Enforced order of x and y axis
    xtype = None
    if q_index_0 in HCS_dtypesWOmc.keys():
        xtype = HCS_dtypesWOmc[q_index_0]
    
    if len(q_index) >1: # multiple choice case
        x_range = data['x_value']
        width = 0.1
    elif xtype == 'category':
        x_range = HCS_orderedCats[q_index_0]
        width = 0.1
    else:
        x_range = None
        width = 0.6
    y_range = None


    ydata_spec['y_keys'] = data_filters
    ydata_spec['colors'] = colors
    ydata_spec['legend_labels'] = data_filters
    selected = ColumnDataSource(data=data)
    ydata_spec = ColumnDataSource(data=ydata_spec)

    display_options = {'x_range' : x_range, 'y_range': y_range,
                       'title': f'{question_full}', 'width': width}
    #print(display_options)
    return selected, ydata_spec, display_options



def select_data_corr(question, question2, data_filters, data_filters_method):
    """Select the data to display in the correlation vis"""

    q1_key = map_question_to_qkey(question)
    q2_key = map_question_to_qkey(question2)
    q1_index_0 = q1_key[0]
    q2_index_0 = q2_key[0]
    # Enforced order of x and y axis
    # If something is not a category, use default instead 
    xtype = None
    if q1_index_0 in HCS_dtypesWOmc.keys():
        xtype = HCS_dtypesWOmc[q1_index_0]

    if xtype == 'category':
        x_range = HCS_orderedCats[q1_index_0]
    else:
        x_range = None

    ytype = None
    if q2_index_0 in HCS_dtypesWOmc.keys():
        ytype = HCS_dtypesWOmc[q2_index_0]
    if ytype == 'category':
        y_range = HCS_orderedCats[q2_index_0]
    else:
        y_range = None

    q1_key_clean = []
    keys = list(survey_data.keys())
    for key in q1_key:
        if key in keys:
            q1_key_clean.append(key)

    q2_key_clean = []
    for key in q2_key:
        if key in keys:
            q2_key_clean.append(key)

    exclude_nan = True
    if len(q1_key) >1:
        exclude_nan = False

    
    method_include = []
    method_exclude = []
    methods_dict = HCS_MCsubquestions[FILTER_BY_2]
    for method in data_filters_method:
        for key, val in methods_dict.items():
            if val == method:
                method_include.append(key)
                # Filter out the one who provided False
                method_exclude.append((key, [False]))

    exclude_area = []
    for field in re_fields:
        if field not in data_filters:
            pass
            #exclude_area.append(("researchArea", [field]))
    #exclude_areas = ["researchArea", exclude_area]

    include_clean = list(set([FILTER_BY]+ q2_key_clean + q1_key_clean + method_include))

    # If this is slow to calculate each time, it might make sense to calculate all of these 
    # at start up. i.e n^2 tables, with arbitray filters not possible
    df = filter_dataframe(survey_data, include=include_clean, exclude=method_exclude, exclude_nan=exclude_nan)
    
    # if list, merge somehow..., multi column crosstab


    cross_tab = calculate_crosstab(df, q1_index_0, q2_index_0)
    # marker size is radius, we want the Area to be proportional to the value
    # we also scale the markers with the max values are to small, or depending how many Cat, or 
    # figure width...
    marker_scale = 20.0
    cross_tab['markersize'] = percentage_to_area(cross_tab['percentage'], scale_m=marker_scale)
    cross_tab['x_values'] = cross_tab[q1_index_0]
    cross_tab['y_values'] = cross_tab[q2_index_0]
    cross_tab['color'] = ['#A0235A' for i in cross_tab[q2_index_0]]
    
    # for hover tool
    tooltips = [(f"{q1_key[0]}", "@x_values"), 
                    (f"{q2_key[0]}", "@y_values"),
                  ("total", "@total"),
                  ("percentage", "@percentage")]

    title = f''#{q1_key[0]} in dependence to {q2_key[0]}'
    xlabel = f'{question}'
    ylabel = f'{question2}'

    # Bokeh plots need a ColumnDataSource, but this can be initialized from a pandas
    selected = ColumnDataSource(cross_tab)

    display_options = {'x_range' : x_range, 'y_range' : y_range, 'xlabel': xlabel, 'ylabel': ylabel,
                        'title': title, 'tooltips' : tooltips}

    return selected, display_options, marker_scale

def select_data_wordcloud(data_filters, data_filters_method, content=['dataGenMetdataGenMethodSpec_hodSpec_']):
    """
    Filter data for wordcloud from data filters
    """
    word_list = []

    method_include = []
    method_exclude = []
    methods_dict = HCS_MCsubquestions[FILTER_BY_2]
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


    data_include = []
    if 'dataGenMethodSpec_' in content:
        for i, method in enumerate(method_include):
            id_meth = method[-1]
            if id_meth == 'r': # From other
                id_meth = i+1
            data_include.append('dataGenMethodSpec_{}_1'.format(id_meth))
            data_include.append('dataGenMethodSpec_{}_2'.format(id_meth))
            data_include.append('dataGenMethodSpec_{}_3'.format(id_meth))
    else:
        data_include = content
    df = filter_dataframe(survey_data, include=[FILTER_BY]+method_include+data_include, exclude=method_exclude, as_type ='str')
    exclude = []
    for field in re_fields:
        if field not in data_filters:
            exclude.append(field)
    if 'All' in data_filters:
        exclude = []
    for area in exclude:
        df = df[df[FILTER_BY] != area]
    #print(list(df.keys()))
    #print(data_include)
    # prepare word list
    word_list = []
    for method in data_include:
        #print(df[method])
        w_list = [word for word in df[method] if str(word)!='nan']
        word_list = word_list + w_list #ent.replace(' ', '-') # Add '-'


    return word_list


##### Widgets


#### Control widgets

# global filters
# section probably better than tabs..
#tab1 = ("Filter research area", fig)
#tab2 = ("Filter HFG field", fig2)
#filter_tabs = pn.Tabs(*[tab1, tab2])

multi_choice = pn.widgets.MultiChoice(name=md_text_global_filters_widgets[0][LANGUAGE], value=["All"], options=FILTER_OPTIONS['researchArea'])
multi_choice_method = pn.widgets.MultiChoice(name=md_text_global_filters_widgets[1][LANGUAGE], value=[], options=FILTER_OPTIONS['method'])
#multi_choice_hgf_field = pn.widgets.MultiChoice(name="Filter by HGF research field (Each selected will be shown)", value=["All"], options=FILTER_OPTIONS['HGFresearchfield'])
# for careerlevel there can be only one, so we use a Multiselect instead
#select_careerlevel = pn.widgets.Select(name="Filter by career level.", value=[], options=FILTER_OPTIONS['careerLevel'])
#multi_choice_facility = pn.widgets.MultiChoice(name="Filter by career level.", value=[], options=FILTER_OPTIONS['LargeScaleFacility'])

# Bar chart
# D: question select could also be a slider?
# TODO: get filter options for question
question_select = pn.widgets.Select(name=md_text_select_widgets[0][LANGUAGE], value=START_DATA_BAR,
    options=questions)#, description="Select the survey question, which results should be displayed.")

multi_filter = pn.widgets.MultiChoice(name="Filter by data by question specific filter", value=[], 
    options=FILTER_OPTIONS['method'], visible=False)

question_select2 = pn.widgets.Select(name=md_text_select_widgets[1][LANGUAGE], value=START_DATA_BAR2,
    options=questions)#, description="Select the survey question, which results should be displayed.")

multi_filter2 = pn.widgets.MultiChoice(name="Filter by data by question specific filter", value=[], 
    options=FILTER_OPTIONS['method'], visible=False)



# D: better than a Select would be to use the HMC template for this...
# D: Maybe have two dashboards running a German and a English one and link build in the link in the template...
#lang_select = Select(title="Language", value="en",
#               options=['en', 'de'], description="Change the language of the Dashboard.")

chart_select1 =  pn.widgets.Select(title="Visualization type", value="Vertical Bar chart",
               options=['Vertical Bar chart', 'Horizontal Bar chart', 'Pie chart'])
chart_select2 =  pn.widgets.Select(title="Visualization type", value="Vertical Bar chart",
               options=['Vertical Bar chart', 'Horizontal Bar chart', 'Pie chart'])

# Correlation plot
# Not every question can be correlated with every question?
#question_select_corr2 = pn.widgets.Select(name="Question X-Axis", value=START_DATA_CORR_1,
#               options=questions)#, description="Select the survey question which results should be displayed on the X-Axis.")
#question_select_corr3 = pn.widgets.Select(name="Question Y-Axis", value=START_DATA_CORR_2,
#               options=questions)#, description="Select the survey question which results should be displayed on the Y-Axis.")


# Others
plot_aspect_ratio_select = pn.widgets.Select(name="Filter data", value="Cum. Sum",
               options=FILTER_OPTIONS)
menu = ['Barchart', 'Correlation Plot']#('Barchart', 'bar_chart'), ('Correlation Plot', '(corr_plot')]
button_bar = pn.widgets.Select(name="Add a chart", options=menu)


def generate_global_filters():
    g_filters = [multi_choice, multi_choice_method]
    return g_filters


def generate_bar_controls():
    controls_bar = [question_select, multi_filter, chart_select1]
    return controls_bar

#def generate_corr_controls():
#    controls_corr = [question_select_corr2, question_select_corr3]
#    return controls_corr

####################################
# Generate Start figures and panes #
####################################
# TODO, just trigger updates...
data_filters = multi_choice.value
data_filters_method = multi_choice_method.value
print('creating starting figures')

start_display_data, ydata_spec, display_options= select_data(question_select.value, data_filters, data_filters_method)
y_keys = ydata_spec.data['y_keys']
fill_colors = ydata_spec.data['colors']


#fig = pn.pane.Bokeh(bokeh_barchart(start_display_data, y=y_keys, factors=y_keys, legend_labels=y_keys, 
#    fill_color=fill_colors, orientation='vertical', **display_options))

fig_exp1 = pn.pane.Bokeh(bokeh_barchart(start_display_data, y=y_keys, factors=y_keys, legend_labels=y_keys, 
    fill_color=fill_colors, orientation='vertical', **display_options))

start_display_data, ydata_spec, display_options= select_data(question_select2.value, data_filters, data_filters_method)
y_keys = ydata_spec.data['y_keys']
fill_colors = ydata_spec.data['colors']
fig_exp2 = pn.pane.Bokeh(bokeh_barchart(start_display_data, y=y_keys, factors=y_keys, legend_labels=y_keys, 
    fill_color=fill_colors, orientation='vertical', **display_options))

start_corr_data, display_options_corr, marker_scale = select_data_corr(question_select.value, 
    question_select2.value, data_filters, data_filters_method)
fig_corr_1 = bokeh_corr_plot(start_corr_data, **display_options_corr)
fig_corr = pn.pane.Bokeh(fig_corr_1)
leg_corr = pn.pane.Bokeh(create_legend_corr(fig_corr_1, colors=start_corr_data.data['color'], scale_m=marker_scale))

# Overview:

#fig_ov1, fig_ov2, fig_ov3, fig_ov4 = generate_overview()
# for now place holders...
start_display_data, ydata_spec, display_options= select_data(START_DATA_OV1, data_filters, data_filters_method)
y_keys = ydata_spec.data['y_keys']
fig_ov1 = pn.pane.Bokeh(bokeh_barchart(start_display_data, y=y_keys, factors=y_keys, legend_labels=y_keys, 
    fill_color=ydata_spec.data['colors'], orientation='vertical', **display_options))

start_display_data, ydata_spec, display_options= select_data(START_DATA_OV2, data_filters, data_filters_method)
y_keys = ydata_spec.data['y_keys']
fig_ov2 = pn.pane.Bokeh(bokeh_barchart(start_display_data, y=y_keys, factors=y_keys, legend_labels=y_keys, 
    fill_color=ydata_spec.data['colors'], orientation='vertical', **display_options))

start_display_data, ydata_spec, display_options= select_data(START_DATA_OV3, data_filters, data_filters_method)
y_keys = ydata_spec.data['y_keys']
fig_ov3 = pn.pane.Bokeh(bokeh_barchart(start_display_data, y=y_keys, factors=y_keys, legend_labels=y_keys, 
    fill_color=ydata_spec.data['colors'], orientation='vertical', **display_options))

start_display_data, ydata_spec, display_options= select_data(START_DATA_OV4, data_filters, data_filters_method)
y_keys = ydata_spec.data['y_keys']
fig_ov4 = pn.pane.Bokeh(bokeh_barchart(start_display_data, y=y_keys, factors=y_keys, legend_labels=y_keys, 
    fill_color=ydata_spec.data['colors'], orientation='vertical', **display_options))


# Methods, Software and repos

half_width = int(ACCORDION_WIDTH/2)
# Wordcloud of methods #RSDP2b
text_list = select_data_wordcloud(data_filters, data_filters_method, content=["dataGenMethodSpec_"])
wordcloud = generate_wordcloud(text_list, height=DEFAULT_FIGURE_HEIGHT, width=half_width)
svg_pane = pn.pane.Bokeh(interactive_wordcloud(wordcloud), width=wordcloud.width, height=wordcloud.height)
#pn.pane.SVG(wordcloud.to_svg(), width=wordcloud.width, height=wordcloud.height)

# Wordcloud of software #RDMPR10
text_list = select_data_wordcloud(data_filters, data_filters_method, content=["software_1", "software_2", "software_3"])
wordcloud_soft = generate_wordcloud(text_list, height=DEFAULT_FIGURE_HEIGHT, width=half_width)
svg_pane_software = pn.pane.Bokeh(interactive_wordcloud(wordcloud_soft), width=wordcloud.width, height=wordcloud.height)
#pn.pane.SVG(wordcloud_soft.to_svg(), width=wordcloud_soft.width, height=wordcloud_soft.height)

# Wordcloud of repos #DTPUB5
text_list = select_data_wordcloud(data_filters, data_filters_method, content=["pubRepo_1", "pubRepo_2", "pubRepo_3", "pubRepo_4", "pubRepo_5"])
wordcloud_repo = generate_wordcloud(text_list, height=DEFAULT_FIGURE_HEIGHT, width=half_width)
svg_pane_repo = pn.pane.Bokeh(interactive_wordcloud(wordcloud_repo), width=wordcloud.width, height=wordcloud.height)
#pn.pane.SVG(wordcloud_repo.to_svg(), width=wordcloud_repo.width, height=wordcloud_repo.height)


#


def update(target, event, question_sel, f_choice, m_choice, q_filter, charttype):
    """Update the charts
    
    The target will be replaced, the event contains what interaction was trickered.
    Here we assume value change, because no others where allowed.
    """
    print(event)
    question = question_sel#.value
    data_filters = f_choice.value
    data_filters_method = m_choice.value   
    charttype = charttype#.value

    df, ydata_spec, display_options = select_data(question, data_filters, data_filters_method)
    source = df

    y_keys = ydata_spec.data['y_keys']
    fill_colors = ydata_spec.data['colors']
    if charttype == 'Vertical Bar chart':
        fig = bokeh_barchart(source, y=y_keys, factors=y_keys, legend_labels=y_keys, fill_color=fill_colors, orientation='vertical', **display_options)#df.data['factors'], legend_labels='legend_labels')#, figure=figure)
    elif charttype == 'Horizontal Bar chart':
        y_range = display_options['y_range']
        display_options['y_range'] = display_options['x_range']
        display_options['x_range'] = y_range
        # TODO change tooltips...
        fig = bokeh_barchart(source, y=y_keys, factors=y_keys, legend_labels=y_keys, 
        fill_color=fill_colors, orientation='horizontal', xlabel='Number of Answers', ylabel='', **display_options)#'horizontal')#df.data['factors'], legend_labels='legend_labels')#, figure=figure)
    elif charttype == "Pie chart":
        display_options.pop('x_range')
        display_options.pop('y_range')
        display_options.pop('width')
        fig = bokeh_piechart(source, y=y_keys, legend_labels=y_keys, 
        fill_color=fill_colors, **display_options)
    #else:
    #    fig = None
    #    print(f'This chart type does not exists: {charttype}')
    target.object = fig


def update_corr(target, event, question_sel, question_sel2, f_choice, m_choice):
    """Update the correlation plot"""

    print(event)
    print('correlation_plot')
    question = question_sel.value
    question2 = question_sel2.value
    data_filters = f_choice.value
    data_filters_method = m_choice.value
    df, display_options, marker_scale = select_data_corr(question, question2, data_filters, data_filters_method)
    print(df.data)
    print(display_options)
    fig_corr = bokeh_corr_plot(df, **display_options)
    leg_corr = create_legend_corr(fig_corr, colors=df.data['color'], scale_m=marker_scale)

    target.object = fig_corr


def update_wordcloud(target, event, f_choice, m_choice, content):
    """Update the correlation plot"""

    print(event)
    data_filters = f_choice.value
    data_filters_method = m_choice.value

    text_list = select_data_wordcloud(data_filters, data_filters_method, content=content)
    wordcloud = generate_wordcloud(text_list, height=DEFAULT_FIGURE_HEIGHT, width=DEFAULT_FIGURE_WIDTH)
    target.object = interactive_wordcloud(wordcloud)#wordcloud.to_svg()


# TODO It would be better performance wise to filter one time and update all plots
# But I did not figure out how to update a full bunch of things and not only the give instance
# So the update function has to be splitted to archive/cache the filtered data somehow...

def gen_update_overview1(target, event):
    f_choice, m_choice = multi_choice, multi_choice_method
    question_sel = START_DATA_OV1
    update(target, event, question_sel, f_choice, m_choice, q_filter=None, 
        charttype='Vertical Bar chart')

def gen_update_overview2(target, event):
    f_choice, m_choice = multi_choice, multi_choice_method
    question_sel = START_DATA_OV2
    update(target, event, question_sel, f_choice, m_choice, q_filter=None, 
        charttype='Vertical Bar chart')

def gen_update_overview3(target, event):
    f_choice, m_choice = multi_choice, multi_choice_method
    question_sel = START_DATA_OV3
    update(target, event, question_sel, f_choice, m_choice, q_filter=None, 
        charttype='Vertical Bar chart')

def gen_update_overview4(target, event):
    f_choice, m_choice = multi_choice, multi_choice_method
    question_sel = START_DATA_OV4
    update(target, event, question_sel, f_choice, m_choice, q_filter=None, charttype='Vertical Bar chart')

def gen_update_exp1(target, event):
    f_choice, m_choice,  = multi_choice, multi_choice_method
    question_sel, q_filter, charttype = question_select.value, multi_filter, chart_select1.value
    update(target, event, question_sel, f_choice, m_choice, q_filter, charttype)

def gen_update_exp2(target, event):
    f_choice, m_choice,  = multi_choice, multi_choice_method
    question_sel, q_filter, charttype = question_select2.value, multi_filter2, chart_select2.value
    update(target, event, question_sel, f_choice, m_choice, q_filter, charttype)

def gen_update_corr(target, event):
    f_choice, m_choice = multi_choice, multi_choice_method
    question_sel = question_select
    question_sel2 = question_select2
    update_corr(target, event, question_sel, question_sel2, f_choice, m_choice)

def gen_update_wc_methods(target, event):
    f_choice, m_choice = multi_choice, multi_choice_method
    content = ["dataGenMethodSpec_"]
    update_wordcloud(target, event, f_choice, m_choice, content)

def gen_update_wc_software(target, event):
    f_choice, m_choice = multi_choice, multi_choice_method
    content = ["software_1", "software_2", "software_3"]
    update_wordcloud(target, event, f_choice, m_choice, content)

def gen_update_wc_repo(target, event):
    f_choice, m_choice = multi_choice, multi_choice_method
    content = ["pubRepo_1", "pubRepo_2", "pubRepo_3", "pubRepo_4", "pubRepo_5"]
    update_wordcloud(target, event, f_choice, m_choice, content)

# Register Links between widgets and plots and their respective callbacks

g_filters = generate_global_filters()
for control in g_filters:
    control.link(fig_exp1, callbacks={'value': gen_update_exp1})
    control.link(fig_exp2, callbacks={'value': gen_update_exp2})
    control.link(svg_pane, callbacks={'value': gen_update_wc_methods})
    control.link(svg_pane_software, callbacks={'value': gen_update_wc_software})
    control.link(svg_pane_repo, callbacks={'value': gen_update_wc_repo})
    control.link(fig_corr, callbacks={'value': gen_update_corr})
    control.link(fig_ov1, callbacks={'value': gen_update_overview1})
    control.link(fig_ov2, callbacks={'value': gen_update_overview2})
    control.link(fig_ov3, callbacks={'value': gen_update_overview3})
    control.link(fig_ov4, callbacks={'value': gen_update_overview4})

controls_bar = generate_bar_controls()
for control in controls_bar:
    control.link(fig_exp1, callbacks={'value': gen_update_exp1})
    control.link(fig_corr, callbacks={'value': gen_update_corr})

controls_bar2 = [question_select2, multi_filter2, chart_select2]
for control in controls_bar2:
    control.link(fig_exp2, callbacks={'value': gen_update_exp2})
    control.link(fig_corr, callbacks={'value': gen_update_corr})

#controls_corr = generate_corr_controls()
#for control in controls_corr:
#    control.link(fig_corr, callbacks={'value': gen_update_corr})

####################
# Dashboard layout #
####################
print('Creating layout')
# Layout with Panel
# We provide the layout in this explicit way and not all in one list because first 
# we addressed the objects over the rows name, now this may be obsolete



# Global data filters

row1 = pn.Column(md_text_global_filter[LANGUAGE], g_filters[0], g_filters[1], sizing_mode="scale_width")

global_filters_sec = row1

# Overview part
overview_sec = pn.Column(md_text_overview[LANGUAGE], pn.Row(fig_ov3, fig_ov2), pn.Row(fig_ov1, fig_ov4))


# Tools
row4 = pn.Column(md_text_tools_used[LANGUAGE], "## Research and Data Generation Methods :\n", svg_pane, "## Main Software in use:\n", svg_pane_software,"## Repositories Data published in:\n", svg_pane_repo)
methods_tools_sec = row4


# Question Explorer
# Merge Question explorer and Correlation explorer, allow two questions side by side?


# section probably better than tabs..
#tab1 = ("Vertical Bar chart", fig)
#tab2 = ("Horizontal Bar chart", fig2)
#tab3 = ("Pie chart", fig3)
#tabs = construct_tabs([tab1, tab2, tab3])

inputs = pn.Column(*controls_bar, width=half_width)
inputs2 = pn.Column(*controls_bar2, width=half_width)
row2 =  pn.Column(pn.Row(inputs, inputs2), pn.Row(fig_exp1, fig_exp2))
# Correlation 
#inputs_corr = pn.Column(*controls_corr, width=800)
row3 = pn.Column(md_text_corrchart[LANGUAGE], pn.Row(fig_corr, leg_corr))
coree_ex_sec = row3
question_ex_sec = pn.Column(md_text_barchart[LANGUAGE], row2, row3)


#row5 = pn.Row(button_bar)
#layout = pn.Column(row1, md_text_barchart, row2, md_text_corrchart, row3, row4, 
# sizing_mode="scale_both", title='HMC Survey Dashboard')
#md_text_button, row4, sizing_mode="scale_both", title='HMC Survey Dashboard')


# Depending on the layout these could also be in tabs, but then they cannot be viewed together...
overall_accordion = pn.Accordion((accordion_titles[LANGUAGE][0], global_filters_sec),
                                (accordion_titles[LANGUAGE][1], overview_sec),
                                (accordion_titles[LANGUAGE][2], methods_tools_sec),
                                (accordion_titles[LANGUAGE][3], question_ex_sec), sizing_mode="scale_both")#, css_classes=['accordion', 'accordion-header'])#,
                                #('Correlation explorer', coree_ex_sec))
overall_accordion.active = [0,3]#[0,1]
overall_accordion.scroll = True
overall_accordion.margin = 0
overall_accordion.width = ACCORDION_WIDTH
overall_accordion.min_width = ACCORDION_WIDTH

layout = pn.Column(desc, md_text_description[LANGUAGE], overall_accordion)
layout.servable(title='HMC Survey Data Explorer')
print('All done')