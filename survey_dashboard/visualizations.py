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
Visualization manager module for the survey dashboard.
Handles creation and updates of all charts and visualizations.
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
from survey_dashboard.config import (
    DEFAULT_QUESTIONS,
    ACCORDION_WIDTH,
    OFFSET_HEIGHT_FOR_TABS,
    WORDCLOUD_CONTENT,
    SIZING_MODE,
    LANGUAGE
)
from survey_dashboard.text_display import (
    md_text_tools_used,
    md_text_tools_tabs
)


class VisualizationManager:
    """Manages creation and updating of all visualizations."""
    
    def __init__(self, data_processor):
        """Initialize visualization manager with data processor."""
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
    
    def update_chart(self, target, event, question_sel, f_choice, m_choice, q_filter, charttype):
        """Update charts based on user selections."""
        print(event)
        question = question_sel  # .value
        data_filters = f_choice.value
        data_filters_method = m_choice.value
        charttype = charttype  # .value

        df, ydata_spec, display_options = self.data_processor.select_data(
            question, data_filters, data_filters_method
        )
        source = df

        y_keys = ydata_spec.data["y_keys"]
        fill_colors = ydata_spec.data["colors"]
        
        if charttype == "Vertical Bar chart":
            fig = bokeh_barchart(
                source,
                y=y_keys,
                factors=y_keys,
                legend_labels=y_keys,
                fill_color=fill_colors,
                orientation="vertical",
                **display_options,
            )
        elif charttype == "Horizontal Bar chart":
            # Swap the ranges for horizontal orientation
            y_range = display_options["y_range"]
            display_options["y_range"] = display_options["x_range"]
            display_options["x_range"] = y_range

            # Swap the labels for horizontal orientation
            display_options["xlabel"] = ""  # X axis lays vertically but shows categorical data
            display_options["ylabel"] = "Number of Answers"  # Y axis now lays horizontally but still shows numerical data
            
            fig = bokeh_barchart(
                source,
                y=y_keys,
                factors=y_keys,
                legend_labels=y_keys,
                fill_color=fill_colors,
                orientation="horizontal",
                **display_options,
            )
        elif charttype == "Pie chart":
            display_options.pop("x_range")
            display_options.pop("y_range")
            display_options.pop("width")
            fig = bokeh_piechart(
                source,
                y=y_keys,
                legend_labels=y_keys,
                fill_color=fill_colors,
                **display_options,
            )
        
        target.object = fig

    def update_correlation_chart(self, target, event, question_sel, question_sel2, f_choice, m_choice):
        """Update the correlation plot."""
        print(event)
        print("correlation_plot")
        question = question_sel.value
        question2 = question_sel2.value
        data_filters = f_choice.value
        data_filters_method = m_choice.value
        
        df, display_options, marker_scale = self.data_processor.select_data_corr(
            question, question2, data_filters, data_filters_method
        )
        print(df.data)
        print(display_options)
        fig_corr = bokeh_corr_plot(df, **display_options)
        
        target.object = fig_corr

    def update_wordcloud(self, target, event, f_choice, m_choice, content):
        """Update word cloud visualizations."""
        print(event)
        data_filters = f_choice.value
        data_filters_method = m_choice.value

        text_list = self.data_processor.select_data_wordcloud(
            data_filters, data_filters_method, content=content
        )
        wordcloud = generate_wordcloud(
            text_list, height=DEFAULT_FIGURE_HEIGHT, width=DEFAULT_FIGURE_WIDTH
        )
        target.object = interactive_wordcloud(wordcloud)
    
    def create_update_callbacks(self, widgets):
        """Create all update callback functions."""
        # Extract widgets for easier access
        multi_choice = widgets["global_filters"]["research_area"]
        multi_choice_method = widgets["global_filters"]["method"]
        question_select = widgets["exploration"]["question1"]
        question_select2 = widgets["exploration"]["question2"]
        chart_select1 = widgets["exploration"]["chart_type1"]
        chart_select2 = widgets["exploration"]["chart_type2"]
        multi_filter = widgets["exploration"]["filter1"]
        multi_filter2 = widgets["exploration"]["filter2"]
        
        # Create callback functions
        def gen_update_overview1(target, event):
            f_choice, m_choice = multi_choice, multi_choice_method
            question_sel = self.data_processor.map_qkey_to_question(DEFAULT_QUESTIONS["overview"]["ov1"])
            self.update_chart(
                target, event, question_sel, f_choice, m_choice,
                q_filter=None, charttype="Vertical Bar chart"
            )

        def gen_update_overview2(target, event):
            f_choice, m_choice = multi_choice, multi_choice_method
            question_sel = self.data_processor.map_qkey_to_question(DEFAULT_QUESTIONS["overview"]["ov2"])
            self.update_chart(
                target, event, question_sel, f_choice, m_choice,
                q_filter=None, charttype="Vertical Bar chart"
            )

        def gen_update_overview3(target, event):
            f_choice, m_choice = multi_choice, multi_choice_method
            question_sel = self.data_processor.map_qkey_to_question(DEFAULT_QUESTIONS["overview"]["ov3"])
            self.update_chart(
                target, event, question_sel, f_choice, m_choice,
                q_filter=None, charttype="Vertical Bar chart"
            )

        def gen_update_overview4(target, event):
            f_choice, m_choice = multi_choice, multi_choice_method
            question_sel = self.data_processor.map_qkey_to_question(DEFAULT_QUESTIONS["overview"]["ov4"])
            self.update_chart(
                target, event, question_sel, f_choice, m_choice,
                q_filter=None, charttype="Vertical Bar chart"
            )

        def gen_update_exp1(target, event):
            f_choice, m_choice = multi_choice, multi_choice_method
            question_sel, q_filter, charttype = (
                question_select.value,
                multi_filter,
                chart_select1.value,
            )
            self.update_chart(target, event, question_sel, f_choice, m_choice, q_filter, charttype)

        def gen_update_exp2(target, event):
            f_choice, m_choice = multi_choice, multi_choice_method
            question_sel, q_filter, charttype = (
                question_select2.value,
                multi_filter2,
                chart_select2.value,
            )
            self.update_chart(target, event, question_sel, f_choice, m_choice, q_filter, charttype)

        def gen_update_corr(target, event):
            f_choice, m_choice = multi_choice, multi_choice_method
            question_sel = question_select
            question_sel2 = question_select2
            self.update_correlation_chart(target, event, question_sel, question_sel2, f_choice, m_choice)

        def gen_update_wc_methods(target, event):
            f_choice, m_choice = multi_choice, multi_choice_method
            content = WORDCLOUD_CONTENT["methods"]
            self.update_wordcloud(target, event, f_choice, m_choice, content)

        def gen_update_wc_software(target, event):
            f_choice, m_choice = multi_choice, multi_choice_method
            content = WORDCLOUD_CONTENT["software"]
            self.update_wordcloud(target, event, f_choice, m_choice, content)

        def gen_update_wc_repo(target, event):
            f_choice, m_choice = multi_choice, multi_choice_method
            content = WORDCLOUD_CONTENT["repositories"]
            self.update_wordcloud(target, event, f_choice, m_choice, content)
        
        return {
            "overview": [gen_update_overview1, gen_update_overview2, gen_update_overview3, gen_update_overview4],
            "exploration": [gen_update_exp1, gen_update_exp2],
            "correlation": gen_update_corr,
            "wordclouds": [gen_update_wc_methods, gen_update_wc_software, gen_update_wc_repo]
        }