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
Configuration module for the survey dashboard.
Contains all global constants, paths, and configuration settings.
"""

import os
from pathlib import Path
from bokeh.palettes import Category20

from survey_dashboard.plots import DEFAULT_FIGURE_WIDTH
from survey_dashboard.data.display_specifications.hcs_clean_dictionaries import (
    HCSquestions,
    HCS_colnamesDict,
    HCS_MCsubquestions,
)

# Global Configuration
LANGUAGE = os.environ.get("LANGUAGE_DASHBOARD", "EN")
ACCORDION_WIDTH = int(DEFAULT_FIGURE_WIDTH * 2)
SIZING_MODE = "stretch_width"

# Data Configuration
def get_data_path():
    """Get the path to the data file relative to this module"""
    this_folder = Path(__file__).parent
    return this_folder / "data" / "responses_cleaned_mapped_to_publish.csv"

DATAFILE_PATH = str(get_data_path())

# Filter Configuration
FILTER_BY = "researchArea"
FILTER_BY_2 = "dataGenMethod_"

# Research Fields and Colors
RESEARCH_FIELDS = [
    "All",
    "Cum. Sum",
    "Chemistry",
    "Earth Science",
    "Engineering Science",
    "Life Science",
    "Mathematics",
    "Other",
    "Physics",
    "Psychology"
]

# Generate colors for research fields
RESEARCH_AREA_COLORS = {
    field: Category20[len(RESEARCH_FIELDS)][i]
    for i, field in enumerate(RESEARCH_FIELDS)
}

# Default Questions for Startup
DEFAULT_QUESTIONS = {
    "overview": {
        "ov1": "fairFamiliarity",
        "ov2": "yearsInResearch",
        "ov3": "researchArea",
        "ov4": "pubAmount"
    },
    "exploration": {
        "bar1": "careerLevel",
        "bar2": "docStructured",
        "corr1": "careerLevel",
        "corr2": "docStructured"
    }
}

# Tooltips Configuration
TOOLTIPS = [("Title", "@title"), ("Answer", "@x"), ("Number of Answers", "@y")]

# Widget Configuration
CHART_TYPES = ['Vertical Bar chart', 'Horizontal Bar chart', 'Pie chart']

# Word Cloud Content Configuration
WORDCLOUD_CONTENT = {
    "methods": ["dataGenMethodSpec_"],
    "software": ["software_1", "software_2", "software_3"],
    "repositories": ["pubRepo_1", "pubRepo_2", "pubRepo_3", "pubRepo_4", "pubRepo_5"]
}

# Layout Configuration
HALF_WIDTH_OFFSET = 2  # ACCORDION_WIDTH / 2
OFFSET_HEIGHT_FOR_TABS = 40

# Create reverse dictionaries for data mapping
HCS_COLNAMES_REVERT_DICT = {val: key for key, val in HCS_colnamesDict.items()}
HCS_QUESTIONS_REVERT = {}
HCS_QUESTIONS_REVERT[LANGUAGE] = {
    val: key for key, val in HCSquestions[LANGUAGE].items()
}

# Flatten MC subquestions for easier lookup
HCS_MCSUBQUESTIONS_FLATTENED = {}
for key, val in HCS_MCsubquestions.items():
    for ke, va in val.items():
        HCS_MCSUBQUESTIONS_FLATTENED[ke] = va

# Panel Configuration
PANEL_CONFIG = {
    "loading_spinner": "dots",
    "loading_color": "#005AA0"
}

# Template Configuration
def get_template_path():
    """Get the path to the template file based on language"""
    this_folder = Path(__file__).parent
    return this_folder / f"hmc_layout/{LANGUAGE.lower()}_template.html"

def get_assets_path():
    """Get the path to the assets folder"""
    this_folder = Path(__file__).parent
    return this_folder / "hmc_layout" / "assets"
