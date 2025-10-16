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
Chart creation module for the survey dashboard.
Handles creation of all chart types and visualizations.
"""

import panel as pn

from survey_dashboard.plots import (
    bokeh_barchart,
    bokeh_piechart,
    bokeh_corr_plot,
    create_legend_corr,
    generate_wordcloud,
    interactive_wordcloud,
    DEFAULT_FIGURE_WIDTH,
    DEFAULT_FIGURE_HEIGHT
)
from survey_dashboard.core.config import (
    DEFAULT_QUESTIONS,
    ACCORDION_WIDTH,
    OFFSET_HEIGHT_FOR_TABS,
    WORDCLOUD_CONTENT,
    SIZING_MODE,
    LANGUAGE
)
from survey_dashboard.i18n.text_display import (
    md_text_tools_used,
    md_text_tools_tabs
)


class ChartManager:
    """Manages creation of all chart types."""
    
    def __init__(self, data_processor):
        """Initialize chart manager with data processor."""
        self.data_processor = data_processor
        self.half_width = int(ACCORDION_WIDTH / 2)
    
    def create_overview_charts(self, data_filters, data_filters_method):
        """Create all overview charts."""
        overview_charts = {}
        
        # Get overview question mappings
        overview_questions = {
            'ov1': self.data_processor.map_qkey_to_question(DEFAULT_QUESTIONS["overview"]["ov1"]),
            'ov2': self.data_processor.map_qkey_to_question(DEFAULT_QUESTIONS["overview"]["ov2"]),
            'ov3': self.data_processor.map_qkey_to_question(DEFAULT_QUESTIONS["overview"]["ov3"]),
            'ov4': self.data_processor.map_qkey_to_question(DEFAULT_QUESTIONS["overview"]["ov4"])
        }
        
        # Create each overview chart
        for key, question in overview_questions.items():
            start_display_data, ydata_spec, display_options = self.data_processor.select_data(
                question, data_filters, data_filters_method
            )
            y_keys = ydata_spec.data["y_keys"]
            
            overview_charts[key] = pn.pane.Bokeh(
                bokeh_barchart(
                    start_display_data,
                    y=y_keys,
                    factors=y_keys,
                    legend_labels=y_keys,
                    fill_color=ydata_spec.data["colors"],
                    orientation="vertical",
                    **display_options,
                )
            )
        
        return overview_charts
    
    def create_exploration_charts(self, question_select, question_select2, data_filters, data_filters_method):
        """Create exploration charts."""
        # First exploration chart
        start_display_data, ydata_spec, display_options = self.data_processor.select_data(
            question_select.value, data_filters, data_filters_method
        )
        y_keys = ydata_spec.data["y_keys"]
        fill_colors = ydata_spec.data["colors"]
        
        fig_exp1 = pn.pane.Bokeh(
            bokeh_barchart(
                start_display_data,
                y=y_keys,
                factors=y_keys,
                legend_labels=y_keys,
                fill_color=fill_colors,
                orientation="vertical",
                **display_options,
            )
        )
        
        # Second exploration chart
        start_display_data, ydata_spec, display_options = self.data_processor.select_data(
            question_select2.value, data_filters, data_filters_method
        )
        y_keys = ydata_spec.data["y_keys"]
        fill_colors = ydata_spec.data["colors"]
        
        fig_exp2 = pn.pane.Bokeh(
            bokeh_barchart(
                start_display_data,
                y=y_keys,
                factors=y_keys,
                legend_labels=y_keys,
                fill_color=fill_colors,
                orientation="vertical",
                **display_options,
            )
        )
        
        return fig_exp1, fig_exp2
    
    def create_correlation_chart(self, question_select, question_select2, data_filters, data_filters_method):
        """Create correlation chart with legend."""
        start_corr_data, display_options_corr, marker_scale = self.data_processor.select_data_corr(
            question_select.value, question_select2.value, data_filters, data_filters_method
        )
        fig_corr_1 = bokeh_corr_plot(start_corr_data, **display_options_corr)
        fig_corr = pn.pane.Bokeh(fig_corr_1, align="center")
        
        leg_corr = pn.pane.Bokeh(
            create_legend_corr(
                fig_corr_1, colors=start_corr_data.data["color"], scale_m=marker_scale
            ),
            align="center",
        )
        
        return fig_corr, leg_corr
    
    def create_wordcloud_tabs(self, data_filters, data_filters_method):
        """Create word cloud tabs for methods, software, and repositories."""
        wordcloud_panes = {}
        
        # Create word clouds for each content type
        for content_type, content_fields in WORDCLOUD_CONTENT.items():
            text_list = self.data_processor.select_data_wordcloud(
                data_filters, data_filters_method, content=content_fields
            )
            wordcloud = generate_wordcloud(
                text_list, height=DEFAULT_FIGURE_HEIGHT, width=ACCORDION_WIDTH
            )
            wordcloud_panes[content_type] = pn.pane.Bokeh(
                interactive_wordcloud(wordcloud),
                width=wordcloud.width,
                height=wordcloud.height + OFFSET_HEIGHT_FOR_TABS,
            )
        
        # Create tabs
        methods_tabs = pn.Column(
            md_text_tools_used[LANGUAGE],
            pn.Tabs(
                (md_text_tools_tabs["methods"][LANGUAGE], wordcloud_panes["methods"]),
                (md_text_tools_tabs["software"][LANGUAGE], wordcloud_panes["software"]),
                (md_text_tools_tabs["repositories"][LANGUAGE], wordcloud_panes["repositories"]),
            ),
            sizing_mode=SIZING_MODE,
        )
        
        return methods_tabs, wordcloud_panes

    def create_chart(self, question, data_filters, data_filters_method, chart_type):
        """Create a chart of the specified type."""
        df, ydata_spec, display_options = self.data_processor.select_data(
            question, data_filters, data_filters_method
        )

        y_keys = ydata_spec.data["y_keys"]
        fill_colors = ydata_spec.data["colors"]

        if chart_type == "Vertical Bar chart":
            fig = bokeh_barchart(
                df,
                y=y_keys,
                factors=y_keys,
                legend_labels=y_keys,
                fill_color=fill_colors,
                orientation="vertical",
                **display_options,
            )
        elif chart_type == "Horizontal Bar chart":
            # Swap the ranges for horizontal orientation
            y_range = display_options["y_range"]
            display_options["y_range"] = display_options["x_range"]
            display_options["x_range"] = y_range

            # Swap the labels for horizontal orientation
            display_options["xlabel"] = ""  # X axis lays vertically but shows categorical data
            display_options["ylabel"] = "Number of Answers"  # Y axis now lays horizontally but still shows numerical data
            
            fig = bokeh_barchart(
                df,
                y=y_keys,
                factors=y_keys,
                legend_labels=y_keys,
                fill_color=fill_colors,
                orientation="horizontal",
                **display_options,
            )
        elif chart_type == "Pie chart":
            display_options.pop("x_range")
            display_options.pop("y_range")
            display_options.pop("width")
            fig = bokeh_piechart(
                df,
                y=y_keys,
                legend_labels=y_keys,
                fill_color=fill_colors,
                **display_options,
            )
        
        return fig

    def create_correlation_plot(self, question1, question2, data_filters, data_filters_method):
        """Create correlation plot."""
        df, display_options, marker_scale = self.data_processor.select_data_corr(
            question1, question2, data_filters, data_filters_method
        )
        return bokeh_corr_plot(df, **display_options)

    def create_wordcloud(self, data_filters, data_filters_method, content):
        """Create word cloud visualization."""
        text_list = self.data_processor.select_data_wordcloud(
            data_filters, data_filters_method, content=content
        )
        wordcloud = generate_wordcloud(
            text_list, height=DEFAULT_FIGURE_HEIGHT, width=DEFAULT_FIGURE_WIDTH
        )
        return interactive_wordcloud(wordcloud)