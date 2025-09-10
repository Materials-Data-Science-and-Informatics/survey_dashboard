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
Simplified entry point for the HMC Survey Dashboard.
This app.py orchestrates the creation of the dashboard using the new modular structure.
"""

print("Initializing HMC Survey Dashboard...")

# Import core components
from survey_dashboard.core.data import DataProcessor
from survey_dashboard.core.charts import ChartManager

# Import UI components  
from survey_dashboard.ui.widgets import WidgetFactory
from survey_dashboard.ui.layout import LayoutManager
from survey_dashboard.ui.callbacks import CallbackManager

print("Loading configuration and data...")

# Initialize core components
data_processor = DataProcessor()
chart_manager = ChartManager(data_processor)

# Initialize UI components
widget_factory = WidgetFactory(data_processor)
layout_manager = LayoutManager()
callback_manager = CallbackManager(data_processor, chart_manager)

print("Creating widgets...")

# Create all widgets
widgets = widget_factory.create_all_widgets()
control_groups = widget_factory.get_control_groups(widgets)

# Get initial filter values
data_filters = widgets["global_filters"]["research_area"].value
data_filters_method = widgets["global_filters"]["method"].value

print("Creating visualizations...")

# Create all visualizations using chart manager
overview_charts = chart_manager.create_overview_charts(data_filters, data_filters_method)
exploration_charts = chart_manager.create_exploration_charts(
    widgets["exploration"]["question1"], 
    widgets["exploration"]["question2"], 
    data_filters, 
    data_filters_method
)
correlation_chart = chart_manager.create_correlation_chart(
    widgets["exploration"]["question1"],
    widgets["exploration"]["question2"],
    data_filters,
    data_filters_method
)
methods_tools_tabs, wordcloud_panes = chart_manager.create_wordcloud_tabs(data_filters, data_filters_method)

print("Setting up callbacks...")

# Create update callbacks
callbacks = callback_manager.create_update_callbacks(widgets)

# Bind callbacks to widgets and charts
def bind_callbacks():
    """Bind all interactive callbacks to their respective widgets and charts."""
    # Global filter callbacks for overview charts
    for i, chart_key in enumerate(['ov1', 'ov2', 'ov3', 'ov4']):
        widgets["global_filters"]["research_area"].param.watch(
            lambda event, target=overview_charts[chart_key], callback=callbacks["overview"][i]: callback(target, event), 
            "value"
        )
        widgets["global_filters"]["method"].param.watch(
            lambda event, target=overview_charts[chart_key], callback=callbacks["overview"][i]: callback(target, event), 
            "value"  
        )

    # Exploration chart callbacks
    for widget_key in ["question1", "question2", "chart_type1", "chart_type2"]:
        if "question" in widget_key:
            callback_idx = 0 if "1" in widget_key else 1
            target_chart = exploration_charts[callback_idx]
            widgets["exploration"][widget_key].param.watch(
                lambda event, target=target_chart, callback=callbacks["exploration"][callback_idx]: callback(target, event),
                "value"
            )
    
    # Global filter callbacks for exploration charts
    for i, callback in enumerate(callbacks["exploration"]):
        target_chart = exploration_charts[i]
        widgets["global_filters"]["research_area"].param.watch(
            lambda event, target=target_chart, callback=callback: callback(target, event), 
            "value"
        )
        widgets["global_filters"]["method"].param.watch(
            lambda event, target=target_chart, callback=callback: callback(target, event), 
            "value"
        )

    # Correlation chart callbacks
    widgets["exploration"]["question1"].param.watch(
        lambda event, target=correlation_chart[0], callback=callbacks["correlation"]: callback(target, event), 
        "value"
    )
    widgets["exploration"]["question2"].param.watch(
        lambda event, target=correlation_chart[0], callback=callbacks["correlation"]: callback(target, event), 
        "value"
    )
    widgets["global_filters"]["research_area"].param.watch(
        lambda event, target=correlation_chart[0], callback=callbacks["correlation"]: callback(target, event), 
        "value"
    )
    widgets["global_filters"]["method"].param.watch(
        lambda event, target=correlation_chart[0], callback=callbacks["correlation"]: callback(target, event), 
        "value"
    )

    # Word cloud callbacks
    wordcloud_targets = [wordcloud_panes["methods"], wordcloud_panes["software"], wordcloud_panes["repositories"]]
    for i, callback in enumerate(callbacks["wordclouds"]):
        target = wordcloud_targets[i]
        widgets["global_filters"]["research_area"].param.watch(
            lambda event, target=target, callback=callback: callback(target, event), 
            "value"
        )
        widgets["global_filters"]["method"].param.watch(
            lambda event, target=target, callback=callback: callback(target, event), 
            "value"
        )

print("Creating layout...")

# Create complete layout
layout = layout_manager.create_complete_layout(
    control_groups=control_groups,
    overview_charts=overview_charts,
    exploration_charts=exploration_charts,
    correlation_chart=correlation_chart,
    methods_tools_tabs=methods_tools_tabs
)

print("Setting up template...")

# Setup template and make servable
template = layout_manager.setup_template_variables(layout)
bind_callbacks()

print("Dashboard ready! Making servable...")
template = layout_manager.make_servable()

print("HMC Survey Dashboard initialized successfully!")