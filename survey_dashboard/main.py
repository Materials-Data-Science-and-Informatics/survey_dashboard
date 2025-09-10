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
Main entry point for the HMC Survey Dashboard.
This simplified main file orchestrates the creation of the dashboard using
modular components for data processing, widgets, visualizations, and layout.
"""

print("Initializing HMC Survey Dashboard...")

# Import modular components
from survey_dashboard.data_processor import DataProcessor
from survey_dashboard.widgets import WidgetFactory
from survey_dashboard.visualizations import VisualizationManager
from survey_dashboard.layout_manager import LayoutManager

print("Loading configuration and data...")

# Initialize core components
data_processor = DataProcessor()
widget_factory = WidgetFactory(data_processor)
visualization_manager = VisualizationManager(data_processor)
layout_manager = LayoutManager()

print("Creating widgets...")

# Create all widgets
widgets = widget_factory.create_all_widgets()
control_groups = widget_factory.get_control_groups(widgets)

# Get initial filter values
data_filters = widgets["global_filters"]["research_area"].value
data_filters_method = widgets["global_filters"]["method"].value

print("Creating visualizations...")

# Create all visualizations
overview_charts = visualization_manager.create_overview_charts(data_filters, data_filters_method)
exploration_charts = visualization_manager.create_exploration_charts(
    widgets["exploration"]["question1"], 
    widgets["exploration"]["question2"], 
    data_filters, 
    data_filters_method
)
correlation_chart = visualization_manager.create_correlation_chart(
    widgets["exploration"]["question1"], 
    widgets["exploration"]["question2"], 
    data_filters, 
    data_filters_method
)
methods_tools_tabs, wordcloud_panes = visualization_manager.create_wordcloud_tabs(data_filters, data_filters_method)

print("Setting up callbacks...")

# Create callback functions
callbacks = visualization_manager.create_update_callbacks(widgets)

# Link global filters to all charts
global_filters = control_groups["global_filters"]
for control in global_filters:
    # Link to exploration charts
    control.link(exploration_charts[0], callbacks={"value": callbacks["exploration"][0]})
    control.link(exploration_charts[1], callbacks={"value": callbacks["exploration"][1]})
    
    # Link to word clouds
    control.link(wordcloud_panes["methods"], callbacks={"value": callbacks["wordclouds"][0]})
    control.link(wordcloud_panes["software"], callbacks={"value": callbacks["wordclouds"][1]})
    control.link(wordcloud_panes["repositories"], callbacks={"value": callbacks["wordclouds"][2]})
    
    # Link to correlation chart
    control.link(correlation_chart[0], callbacks={"value": callbacks["correlation"]})
    
    # Link to overview charts
    control.link(overview_charts['ov1'], callbacks={"value": callbacks["overview"][0]})
    control.link(overview_charts['ov2'], callbacks={"value": callbacks["overview"][1]})
    control.link(overview_charts['ov3'], callbacks={"value": callbacks["overview"][2]})
    control.link(overview_charts['ov4'], callbacks={"value": callbacks["overview"][3]})

# Link exploration controls to charts
controls_bar1 = control_groups["controls_bar1"]
for control in controls_bar1:
    control.link(exploration_charts[0], callbacks={"value": callbacks["exploration"][0]})
    control.link(correlation_chart[0], callbacks={"value": callbacks["correlation"]})

controls_bar2 = control_groups["controls_bar2"]
for control in controls_bar2:
    control.link(exploration_charts[1], callbacks={"value": callbacks["exploration"][1]})
    control.link(correlation_chart[0], callbacks={"value": callbacks["correlation"]})

print("Creating layout...")

# Create complete layout
layout = layout_manager.create_complete_layout(
    control_groups=control_groups,
    overview_charts=overview_charts,
    exploration_charts=exploration_charts,
    correlation_chart=correlation_chart,
    methods_tools_tabs=methods_tools_tabs
)

# Setup template and make servable
template = layout_manager.setup_template_variables(layout)
layout_manager.make_servable()

print("Dashboard ready! 🎉")
print("Serve with: panel serve --port 5006 survey_dashboard/ --static-dirs en_files=./survey_dashboard/hmc_layout/static/en_files")