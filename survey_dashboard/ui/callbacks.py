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
Callbacks module for the survey dashboard.
Handles all interactive update callbacks for charts and visualizations.
"""

from survey_dashboard.core.config import DEFAULT_QUESTIONS, WORDCLOUD_CONTENT
from survey_dashboard.core.charts import ChartManager


class CallbackManager:
    """Manages all callback functions for interactive updates."""

    def __init__(self, data_processor, chart_manager, widget_factory):
        """
        Initialize callback manager with data processor, chart manager, and widget factory.

        Args:
            data_processor: DataProcessor instance for data operations
            chart_manager: ChartManager instance for chart creation
            widget_factory: WidgetFactory instance for question key lookups (required for validation)
        """
        self.data_processor = data_processor
        self.chart_manager = chart_manager
        self.widget_factory = widget_factory
        self.correlation_row = None  # Will be set via set_correlation_row()

    def set_correlation_row(self, correlation_row):
        """
        Store reference to correlation row for visibility toggling.

        Args:
            correlation_row: Panel Column containing the correlation section
        """
        self.correlation_row = correlation_row

    def _check_both_questions_compatible(self, question1_text, question2_text):
        """
        Check if both questions are correlation-compatible.

        Args:
            question1_text: Display text from question selector 1 (may have ★)
            question2_text: Display text from question selector 2 (may have ★)

        Returns:
            bool: True if both questions can be used in correlation plot

        Raises:
            RuntimeError: If widget_factory was not provided during initialization
        """
        from survey_dashboard.data.hcs_clean_dictionaries import corr_chart_allowed

        # Fail fast if widget_factory wasn't provided (programming error)
        if not self.widget_factory:
            raise RuntimeError(
                "CallbackManager requires widget_factory for question validation. "
                "Pass widget_factory to CallbackManager.__init__()"
            )

        try:
            # Get internal keys for both questions using the source of truth
            key1 = self.widget_factory.get_question_key(question1_text)
            key2 = self.widget_factory.get_question_key(question2_text)

            # Check if both are in the allowed list
            both_compatible = (key1 in corr_chart_allowed and key2 in corr_chart_allowed)
            return both_compatible

        except Exception as e:
            # If we can't determine, hide correlation (safe default)
            return False

    def update_chart(self, target, event, question_sel, f_choice, m_choice, q_filter, charttype):
        """Update charts based on user selections."""
        question = question_sel
        data_filters = f_choice.value
        data_filters_method = m_choice.value
        charttype = charttype

        fig = self.chart_manager.create_chart(question, data_filters, data_filters_method, charttype)
        target.object = fig

    def update_correlation_chart(self, target, event, question_sel, question_sel2, f_choice, m_choice):
        """Update the correlation plot and toggle visibility based on question compatibility."""
        question = question_sel.value
        question2 = question_sel2.value

        # Check if both questions are correlation-compatible
        both_compatible = self._check_both_questions_compatible(question, question2)

        # Toggle visibility of correlation section
        if self.correlation_row is not None:
            self.correlation_row.visible = both_compatible

        # Only update the plot if both questions are compatible (performance optimization)
        if both_compatible:
            data_filters = f_choice.value
            data_filters_method = m_choice.value

            fig_corr = self.chart_manager.create_correlation_plot(
                question, question2, data_filters, data_filters_method
            )
            target.object = fig_corr

    def update_wordcloud(self, target, event, f_choice, m_choice, content):
        """Update word cloud visualizations."""
        data_filters = f_choice.value
        data_filters_method = m_choice.value

        wordcloud = self.chart_manager.create_wordcloud(data_filters, data_filters_method, content)
        target.object = wordcloud
    
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