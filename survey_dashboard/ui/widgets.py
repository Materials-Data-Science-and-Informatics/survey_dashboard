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
Widget factory module for the survey dashboard.
Creates and manages all interactive widgets used in the dashboard.
"""

import panel as pn

from survey_dashboard.core.config import (
    LANGUAGE,
    CHART_TYPES,
    DEFAULT_QUESTIONS,
)
from survey_dashboard.i18n.text_display import (
    md_text_global_filters_widgets,
    md_text_select_widgets
)
from survey_dashboard.data.hcs_clean_dictionaries import (
    FILTER_OPTIONS,
    BARCHART_ALLOWED,
    corr_chart_allowed
)


class WidgetFactory:
    """Factory class for creating dashboard widgets."""

    def __init__(self, data_processor):
        """Initialize widget factory with data processor for question mapping."""
        self.data_processor = data_processor

        # Create question list with visual indicators for correlation-compatible questions
        # Also maintain a mapping from display text to internal key
        self.questions = []
        self.question_to_key = {}  # Maps display text (with ★) -> internal key

        for key in BARCHART_ALLOWED:
            question_text = self.data_processor.map_qkey_to_question(key)

            # Add ★ indicator for correlation-compatible questions
            if key in corr_chart_allowed:
                display_text = f"★ {question_text}"
            else:
                display_text = question_text

            self.questions.append(display_text)
            self.question_to_key[display_text] = key

    def _get_display_text_for_key(self, key):
        """
        Get the display text (with ★ if applicable) for a given question key.

        Args:
            key: Internal question key (e.g., 'careerLevel')

        Returns:
            Display text with ★ prefix if correlation-compatible
        """
        question_text = self.data_processor.map_qkey_to_question(key)
        if key in corr_chart_allowed:
            return f"★ {question_text}"
        return question_text

    def get_question_key(self, display_text):
        """
        Get the internal key for a question from its display text.
        Handles both decorated (★) and plain text.

        Args:
            display_text: Question text as shown in dropdown (may have ★)

        Returns:
            Internal question key (e.g., 'careerLevel')
        """
        return self.question_to_key.get(display_text)

    def is_correlation_compatible(self, display_text):
        """
        Check if a question is correlation-compatible.

        Args:
            display_text: Question text as shown in dropdown (may have ★)

        Returns:
            True if the question can be used in correlation plots
        """
        key = self.get_question_key(display_text)
        return key in corr_chart_allowed if key else False

    def create_global_filters(self):
        """Create global filter widgets."""
        multi_choice = pn.widgets.MultiChoice(
            name=md_text_global_filters_widgets[0][LANGUAGE],
            value=["All"],
            options=FILTER_OPTIONS["researchArea"],
        )

        multi_choice_method = pn.widgets.MultiChoice(
            name=md_text_global_filters_widgets[1][LANGUAGE],
            value=[],
            options=FILTER_OPTIONS["method"],
        )

        return [multi_choice, multi_choice_method]

    def create_question_selectors(self):
        """Create question selector widgets for exploration charts."""
        # Get default question keys
        default_key1 = DEFAULT_QUESTIONS["exploration"]["bar1"]
        default_key2 = DEFAULT_QUESTIONS["exploration"]["bar2"]

        # Find the display text (with ★ if applicable) that matches the default key
        default_value1 = self._get_display_text_for_key(default_key1)
        default_value2 = self._get_display_text_for_key(default_key2)

        question_select = pn.widgets.Select(
            name=md_text_select_widgets[0][LANGUAGE],
            value=default_value1,
            options=self.questions
        )

        question_select2 = pn.widgets.Select(
            name=md_text_select_widgets[1][LANGUAGE],
            value=default_value2,
            options=self.questions
        )

        return question_select, question_select2

    def create_chart_type_selectors(self):
        """Create chart type selector widgets."""
        chart_select1 = pn.widgets.Select(
            name="Visualization type",
            value="Vertical Bar chart",
            options=CHART_TYPES
        )

        chart_select2 = pn.widgets.Select(
            name="Visualization type",
            value="Vertical Bar chart",
            options=CHART_TYPES
        )

        return chart_select1, chart_select2

    def create_hidden_filters(self):
        """Create hidden filter widgets (currently not used but kept for compatibility)."""
        multi_filter = pn.widgets.MultiChoice(
            name="Filter by data by question specific filter",
            value=[],
            options=FILTER_OPTIONS["method"],
            visible=False,
        )

        multi_filter2 = pn.widgets.MultiChoice(
            name="Filter by data by question specific filter",
            value=[],
            options=FILTER_OPTIONS["method"],
            visible=False,
        )

        return multi_filter, multi_filter2

    def create_all_widgets(self):
        """Create all widgets and return them organized by type."""
        # Global filters
        global_filters = self.create_global_filters()
        multi_choice, multi_choice_method = global_filters

        # Question selectors
        question_select, question_select2 = self.create_question_selectors()

        # Chart type selectors
        chart_select1, chart_select2 = self.create_chart_type_selectors()

        # Hidden filters
        multi_filter, multi_filter2 = self.create_hidden_filters()

        # Organize widgets
        widgets = {
            "global_filters": {
                "research_area": multi_choice,
                "method": multi_choice_method
            },
            "exploration": {
                "question1": question_select,
                "question2": question_select2,
                "chart_type1": chart_select1,
                "chart_type2": chart_select2,
                "filter1": multi_filter,  # hidden
                "filter2": multi_filter2  # hidden
            }
        }

        return widgets

    def get_control_groups(self, widgets):
        """Get organized control groups for layout."""
        # Global filters group
        global_filters = [
            widgets["global_filters"]["research_area"],
            widgets["global_filters"]["method"]
        ]

        # Bar chart controls for chart 1
        controls_bar1 = [
            widgets["exploration"]["question1"],
            widgets["exploration"]["filter1"],
            widgets["exploration"]["chart_type1"]
        ]

        # Bar chart controls for chart 2
        controls_bar2 = [
            widgets["exploration"]["question2"],
            widgets["exploration"]["filter2"],
            widgets["exploration"]["chart_type2"]
        ]

        return {
            "global_filters": global_filters,
            "controls_bar1": controls_bar1,
            "controls_bar2": controls_bar2
        }
