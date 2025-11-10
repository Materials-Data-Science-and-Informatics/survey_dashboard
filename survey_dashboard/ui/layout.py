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
Layout manager module for the survey dashboard.
Handles the creation and organization of the dashboard layout and template integration.
"""

import panel as pn
from jinja2 import Environment, FileSystemLoader

from survey_dashboard.core.config import (
    LANGUAGE,
    PANEL_CONFIG,
    DEFAULT_QUESTIONS,
    get_template_path,
    get_assets_path
)
from survey_dashboard.i18n.text_display import (
    md_text_global_filter,
    md_text_overview,
    md_text_barchart,
    md_text_corrchart,
    md_text_title,
    md_dashboard_title,
    accordion_titles,
    md_text_descriptions_icons
)
from survey_dashboard.hmc_layout.hmc_custom_layout import (
    hmc_custom_css_accordion,
)
from survey_dashboard.data.hcs_clean_dictionaries import (
    corr_chart_allowed
)


class LayoutManager:
    """Manages the dashboard layout and template integration."""

    def __init__(self):
        """Initialize layout manager and configure Panel."""
        self.correlation_row = None  # Will be set during layout creation
        self.setup_panel_config()
        self.setup_template()
        self.setup_overview_icons()

    def setup_panel_config(self):
        """Configure Panel global settings."""
        pn.config.loading_spinner = PANEL_CONFIG["loading_spinner"]
        pn.config.loading_color = PANEL_CONFIG["loading_color"]
        pn.config.raw_css = [hmc_custom_css_accordion]

    def setup_template(self):
        """Setup Jinja2 template for the dashboard."""
        template_path = get_template_path()
        # Set the loader to look in the directory containing the template
        env = Environment(loader=FileSystemLoader(template_path.parent))
        jinja_template = env.get_template(template_path.name)
        self.template = pn.Template(jinja_template)

    def setup_overview_icons(self):
        """Create overview icons with SVG images."""
        assets_path = get_assets_path()

        people_ic = pn.Row(
            pn.pane.SVG(assets_path / "people.svg"),
            md_text_descriptions_icons["people"][LANGUAGE],
        )
        inst_ic = pn.Row(
            pn.pane.SVG(assets_path / "institute.svg"),
            md_text_descriptions_icons["institution"][LANGUAGE],
        )
        questions_ic = pn.Row(
            pn.pane.SVG(assets_path / "quiz_black_48dp.svg"),
            md_text_descriptions_icons["questions"][LANGUAGE],
        )

        self.overview_icons = pn.Row(people_ic, inst_ic, questions_ic)

    def create_global_filters_section(self, control_groups):
        """Create the global filters section."""
        global_filters_sec = pn.Column(
            md_text_global_filter[LANGUAGE],
            control_groups["global_filters"][0],
            control_groups["global_filters"][1],
            sizing_mode="stretch_width"
        )
        return global_filters_sec

    def create_overview_section(self, overview_charts):
        """Create the overview section with charts."""
        overview_sec = pn.Column(
            md_text_overview[LANGUAGE],
            pn.Row(overview_charts['ov3'], overview_charts['ov2'], sizing_mode="stretch_width"),
            pn.Row(overview_charts['ov1'], overview_charts['ov4'], sizing_mode="stretch_width"),
            sizing_mode="stretch_width",
        )
        return overview_sec

    def create_question_explorer_section(self, control_groups, exploration_charts, correlation_chart):
        """Create the question explorer section with exploration and correlation charts."""
        half_width = 400  # Approximate half width for controls

        # Control inputs
        inputs = pn.Column(*control_groups["controls_bar1"], width=half_width)
        inputs2 = pn.Column(*control_groups["controls_bar2"], width=half_width)

        # Charts row with controls and visualizations
        charts_row = pn.Column(
            pn.Row(inputs, inputs2, sizing_mode="stretch_width"),
            pn.Row(exploration_charts[0], exploration_charts[1], sizing_mode="stretch_width"),
            sizing_mode="stretch_width"
        )

        # Determine initial visibility of correlation section
        # Check if both default questions are correlation-compatible
        default_q1 = DEFAULT_QUESTIONS["exploration"]["bar1"]
        default_q2 = DEFAULT_QUESTIONS["exploration"]["bar2"]

        try:
            initial_visible = (default_q1 in corr_chart_allowed and
                             default_q2 in corr_chart_allowed)
        except:
            # If we can't determine compatibility, hide by default
            initial_visible = False

        # Correlation section (conditionally visible)
        fig_corr, leg_corr = correlation_chart
        correlation_row = pn.Column(
            md_text_corrchart[LANGUAGE],
            pn.Row(
                pn.layout.VSpacer(),
                fig_corr,
                leg_corr,
                pn.layout.VSpacer(),
                sizing_mode="stretch_width"
            ),
            sizing_mode="stretch_width",
            visible=initial_visible  # Set initial visibility based on default questions
        )

        # Combined question explorer section
        question_ex_sec = pn.Column(
            md_text_barchart[LANGUAGE],
            charts_row,
            correlation_row,
            sizing_mode="stretch_width"
        )

        return question_ex_sec, correlation_row  # Return both section and correlation reference

    def create_accordion_layout(self, sections):
        """Create the main accordion layout."""
        overall_accordion = pn.Accordion(
            (accordion_titles[LANGUAGE][0], sections["global_filters"]),
            (accordion_titles[LANGUAGE][1], sections["overview"]),
            (accordion_titles[LANGUAGE][2], sections["methods_tools"]),
            (accordion_titles[LANGUAGE][3], sections["question_explorer"]),
            sizing_mode="stretch_both",
        )

        # Configure accordion settings
        overall_accordion.active = [0, 3]  # Open global filters and question explorer by default
        overall_accordion.scroll = True
        overall_accordion.margin = (20, 20, 20, 20)  # Add consistent margin on all sides
        overall_accordion.width = None  # Remove fixed width constraint
        overall_accordion.min_width = None  # Remove min-width constraint

        return overall_accordion

    def create_complete_layout(self, control_groups, overview_charts, exploration_charts,
                             correlation_chart, methods_tools_tabs):
        """Create the complete dashboard layout."""
        # Create question explorer section and capture correlation_row reference
        question_explorer_section, correlation_row = self.create_question_explorer_section(
            control_groups, exploration_charts, correlation_chart
        )

        # Store correlation_row for later access by callbacks
        self.correlation_row = correlation_row

        # Create all sections
        sections = {
            "global_filters": self.create_global_filters_section(control_groups),
            "overview": self.create_overview_section(overview_charts),
            "methods_tools": methods_tools_tabs,
            "question_explorer": question_explorer_section
        }

        # Create accordion
        accordion = self.create_accordion_layout(sections)

        # Main layout container
        layout = pn.Column(accordion, sizing_mode="stretch_both")

        return layout  # Return only layout - no breaking change to app.py

    def get_correlation_row(self):
        """
        Get reference to the correlation row for callback binding.

        Returns:
            Panel Column containing the correlation plot section, or None if not yet created.
        """
        return self.correlation_row

    def setup_template_variables(self, layout):
        """Setup template with layout and variables."""
        self.template.add_panel("App", layout)
        self.template.add_variable("app_title", md_text_title[LANGUAGE])
        self.template.add_variable("dashboard_title", md_dashboard_title[LANGUAGE])
        self.template.add_variable("image_url", "./en_files/Banner.png")

        return self.template

    def make_servable(self):
        """Make the template servable."""
        self.template.servable(title=md_text_title[LANGUAGE])
        return self.template
