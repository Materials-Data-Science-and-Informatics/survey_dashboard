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
Data processing module for the survey dashboard.
Handles all survey data filtering, transformation, and preparation for visualization.
"""

import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource

from survey_dashboard.analysis import (
    calculate_crosstab,
    prepare_data_research_field,
    filter_dataframe,
    percentage_to_area,
    get_all_values
)
from survey_dashboard.data.hcs_clean_dictionaries import (
    HCSquestions,
    HCS_orderedCats,
    HCS_MCsubquestions,
    HCS_colnamesDict,
    HCS_MCList,
    HCS_dtypesWOmc
)
from survey_dashboard.core.config import (
    LANGUAGE,
    DATAFILE_PATH,
    FILTER_BY,
    FILTER_BY_2,
    RESEARCH_FIELDS,
    RESEARCH_AREA_COLORS,
    HCS_COLNAMES_REVERT_DICT,
    HCS_QUESTIONS_REVERT,
    HCS_MCSUBQUESTIONS_FLATTENED
)


class DataProcessor:
    """Handles all survey data operations and transformations."""
    
    def __init__(self):
        """Initialize the data processor with survey data."""
        self.survey_data = pd.read_csv(DATAFILE_PATH)
        # Rename columns to human readable names
        self.survey_data.rename(columns=HCS_colnamesDict, inplace=True)
        
        # Create data sources for different uses
        self.source = ColumnDataSource(self.survey_data)
        self.source_corr = ColumnDataSource(self.survey_data)
    
    def map_qkey_to_question(self, key: str, lang: str = LANGUAGE) -> str:
        """
        Given a key return the full question to be displayed associated with the key for a given language
        """
        mc_key = key

        if key in HCS_MCList:
            # Multiple choice, all have the same question for now
            mc_key = list(HCS_MCsubquestions[key].keys())[0]
            index = HCS_COLNAMES_REVERT_DICT[mc_key].split("/")[0]
        else:
            index = HCS_COLNAMES_REVERT_DICT[mc_key]

        return HCSquestions[lang][index]

    def map_question_to_qkey(self, question: str, lang: str = LANGUAGE) -> list:
        """
        Map a given question String to the corresponding columns keys in the dataframe

        usually this is one column, but for multiple choice this can be several columns.
        Handles question strings with or without the ★ correlation indicator prefix.
        """
        column_keys = []
        # Strip the ★ indicator if present (used to mark correlation-compatible questions)
        clean_question = question.replace("★ ", "")
        key = HCS_QUESTIONS_REVERT[lang][clean_question]
        if key in HCS_MCList:
            # for multiple choice this is a list of subquestions
            key_s = key + "/"
            for key in HCS_colnamesDict.keys():
                if key_s in key:
                    if not "other" in key:  # for now, needs to be included in HCS_MCsubquestions
                        column_keys.append(HCS_colnamesDict[key])
            column_keys.sort()  # Wrong sort... _1 _10 _2 ...
        else:
            column_keys.append(HCS_colnamesDict[key])
        return column_keys

    def select_data(self, question, data_filters, data_filters_method, filter_by=FILTER_BY):
        """Select and transform data for visualization"""

        def get_real_research_areas(data_filters):
            """
            Separate pseudo-categories (All, Cum. Sum) from real research area values.

            Args:
                data_filters: List of selected filter values

            Returns:
                tuple: (real_research_areas, pseudo_categories)
            """
            pseudo_categories = {"All", "Cum. Sum"}
            real_areas = [area for area in data_filters if area not in pseudo_categories]
            pseudo_cats = [area for area in data_filters if area in pseudo_categories]
            return real_areas, pseudo_cats

        q_index = self.map_question_to_qkey(question)
        q_index_0 = q_index[0]
        # Strip ★ indicator for cleaner chart titles
        question_full = question.replace("★ ", "")

        # Clean up missing columns
        q_index_clean = []
        keys = list(self.survey_data.keys())
        for key in q_index:
            if key in keys:
                q_index_clean.append(key)

        exclude_nan = True
        if len(q_index) > 1:
            exclude_nan = False

        # Process method filters
        method_include = []
        method_exclude = []
        methods_dict = HCS_MCsubquestions[FILTER_BY_2]
        for method in data_filters_method:
            for key, val in methods_dict.items():
                if val == method:
                    method_include.append(key)
                    method_exclude.append((key, [False]))

        include_clean = list(set([FILTER_BY] + q_index_clean + method_include))
        
        # Filter dataframe
        df = filter_dataframe(
            self.survey_data,
            include=include_clean,
            exclude=method_exclude,
            exclude_nan=exclude_nan,
        )
        
        data_all = get_all_values(
            df, q_index_clean, display_dict=HCS_MCSUBQUESTIONS_FLATTENED
        )

        # Separate real research areas from pseudo-categories
        real_research_areas, pseudo_categories = get_real_research_areas(data_filters)

        # Handle data filtering based on what's selected
        if "All" in data_filters and len(data_filters) == 1:
            # Only "All" is selected - use the aggregated data from all research areas
            if len(q_index_clean) == 1:
                key = q_index_clean[0]
                data = {
                    "All": data_all["All"],
                    key: data_all.get(key, []),
                    "x_value": data_all.get(key, [])
                }
                y_keys = ["All"]
            else:
                # Multiple columns case (multiple-choice questions)
                data = data_all.copy()
                # For multiple-choice, get_all_values returns {All: values, last_key: labels}
                # We need to add x_value for the plotting code
                # The last key in q_index_clean contains the x-axis labels
                last_key = q_index_clean[-1]
                if last_key in data_all and "x_value" not in data:
                    data["x_value"] = data_all[last_key]
                y_keys = data_filters
        else:
            # Handle filtering based on real research areas (not pseudo-categories)
            if real_research_areas:
                # Real research areas are selected - filter the data to include only those
                exclude = []
                for field in RESEARCH_FIELDS:
                    # Only exclude fields that are real research areas (not pseudo-categories)
                    if field not in {"All", "Cum. Sum"} and field not in real_research_areas:
                        exclude.append(field)

                for filter_key in exclude:
                    df = df[df[filter_by] != filter_key]
            # else: Only pseudo-categories selected - df remains unfiltered

            # Special case: if we're querying the research area question itself,
            # we need different logic to avoid double-grouping by research areas
            if q_index_0 == filter_by:  # This is the research area question
                # For research area distribution, create data structure directly
                data = {}
                # Use the full research area list as x_value for proper positioning
                data["x_value"] = data_all.get(q_index_0, [])

                # Create arrays for each real research area selected
                for area in real_research_areas:
                    # Create array with value at correct position, zeros elsewhere
                    area_array = np.zeros(len(data["x_value"]))
                    if area in data["x_value"]:
                        position = data["x_value"].index(area)
                        area_count = len(df[df[filter_by] == area])
                        area_array[position] = area_count
                    data[area] = area_array

                # Handle "Cum. Sum" pseudo-category if selected
                if "Cum. Sum" in pseudo_categories:
                    # Add cumulative sum data (this will be the total across all areas)
                    data["Cum. Sum"] = data_all.get("All", [])

                # Set y_keys to include both real areas and pseudo-categories
                y_keys = real_research_areas + [cat for cat in pseudo_categories if cat != "All"]
            else:
                # Normal case: use prepare_data_research_field for other questions
                data, y_keys = prepare_data_research_field(df, q_index)

            # Add "All" data if it's selected in the pseudo-categories
            if "All" in pseudo_categories:
                all_data = data_all.get("All", [])

                # Special handling for research area question
                if q_index_0 == filter_by:  # This is the research area question
                    # Add "All" data to our research area structure
                    data["All"] = all_data
                    # Make sure "All" is in y_keys
                    if "All" not in y_keys:
                        y_keys = ["All"] + y_keys
                elif "researchArea" in data:
                    # When "All" + specific filters are selected, expand to show all research areas
                    # Use full "All" data and expand x_value to all research areas
                    data["All"] = all_data
                    data["x_value"] = data_all["researchArea"]

                    # Expand specific research area data to match full x_value length
                    for key in data_filters:
                        if key != "All" and key in data:
                            # Find position of this research area in full x_value
                            try:
                                position = data["x_value"].index(key)
                                # Create array with value at correct position, zeros elsewhere
                                new_array = np.zeros(len(data["x_value"]), dtype=data[key].dtype)
                                new_array[position] = data[key][0]  # Use first (and only) value
                                data[key] = new_array
                            except ValueError:
                                # If not found, just pad with zeros
                                padding = [0] * (len(data["x_value"]) - len(data[key]))
                                data[key] = list(data[key]) + padding
                else:
                    # For other questions: truncate to match x_value length
                    if len(all_data) > len(data["x_value"]):
                        data["All"] = all_data[:len(data["x_value"])]
                    else:
                        data["All"] = all_data

            # Also expand Cum. Sum to match the new x_value length
            if "Cum. Sum" in data:
                cum_sum_data = data["Cum. Sum"]
                if len(cum_sum_data) < len(data["x_value"]):
                    # Pad with zeros to match new length
                    if isinstance(cum_sum_data, np.ndarray):
                        padding = np.zeros(len(data["x_value"]) - len(cum_sum_data), dtype=cum_sum_data.dtype)
                        data["Cum. Sum"] = np.concatenate([cum_sum_data, padding])
                    else:
                        padding = [0] * (len(data["x_value"]) - len(cum_sum_data))
                        data["Cum. Sum"] = list(cum_sum_data) + padding

        # Prepare display specifications
        ydata_spec = {}
        colors = []
        for key in y_keys:
            colors.append(RESEARCH_AREA_COLORS[key])

        # Determine axis configuration
        xtype = None
        if q_index_0 in HCS_dtypesWOmc.keys():
            xtype = HCS_dtypesWOmc[q_index_0]

        if len(q_index) > 1:  # multiple choice case
            # Defensive: ensure x_value exists, fallback to using q_index_0 data
            x_range = data.get("x_value", data.get(q_index_0, []))
            width = 0.1
        elif xtype == "category":
            x_range = HCS_orderedCats[q_index_0]
            width = 0.1
        else:
            x_range = None
            width = 0.6
        y_range = None

        ydata_spec["y_keys"] = y_keys
        ydata_spec["colors"] = colors
        ydata_spec["legend_labels"] = y_keys
        selected = ColumnDataSource(data=data)
        ydata_spec = ColumnDataSource(data=ydata_spec)

        display_options = {
            "x_range": x_range,
            "y_range": y_range,
            "title": f"{question_full}",
            "width": width,
        }

        return selected, ydata_spec, display_options

    def select_data_corr(self, question, question2, data_filters, data_filters_method):
        """Select the data to display in the correlation vis"""
        q1_key = self.map_question_to_qkey(question)
        q2_key = self.map_question_to_qkey(question2)
        q1_index_0 = q1_key[0]
        q2_index_0 = q2_key[0]
        
        # Determine axis ranges and types
        xtype = None
        if q1_index_0 in HCS_dtypesWOmc.keys():
            xtype = HCS_dtypesWOmc[q1_index_0]

        if xtype == "category":
            x_range = HCS_orderedCats[q1_index_0]
        else:
            x_range = None

        ytype = None
        if q2_index_0 in HCS_dtypesWOmc.keys():
            ytype = HCS_dtypesWOmc[q2_index_0]
        if ytype == "category":
            y_range = HCS_orderedCats[q2_index_0]
        else:
            y_range = None

        # Clean up missing columns
        q1_key_clean = []
        keys = list(self.survey_data.keys())
        for key in q1_key:
            if key in keys:
                q1_key_clean.append(key)

        q2_key_clean = []
        for key in q2_key:
            if key in keys:
                q2_key_clean.append(key)

        exclude_nan = True
        if len(q1_key) > 1:
            exclude_nan = False

        # Process method filters
        method_include = []
        method_exclude = []
        methods_dict = HCS_MCsubquestions[FILTER_BY_2]
        for method in data_filters_method:
            for key, val in methods_dict.items():
                if val == method:
                    method_include.append(key)
                    method_exclude.append((key, [False]))

        include_clean = list(
            set([FILTER_BY] + q2_key_clean + q1_key_clean + method_include)
        )

        # Filter dataframe
        df = filter_dataframe(
            self.survey_data,
            include=include_clean,
            exclude=method_exclude,
            exclude_nan=exclude_nan,
        )

        # Calculate cross-tabulation
        cross_tab = calculate_crosstab(df, q1_index_0, q2_index_0)
        marker_scale = 20.0
        cross_tab["markersize"] = percentage_to_area(
            cross_tab["percentage"], scale_m=marker_scale
        )
        cross_tab["x_values"] = cross_tab[q1_index_0]
        cross_tab["y_values"] = cross_tab[q2_index_0]
        cross_tab["color"] = ["#A0235A" for i in cross_tab[q2_index_0]]

        # Configure tooltips
        tooltips = [
            (f"{q1_key[0]}", "@x_values"),
            (f"{q2_key[0]}", "@y_values"),
            ("total", "@total"),
            ("percentage", "@percentage"),
        ]

        title = f""
        # Strip ★ indicator for cleaner axis labels
        xlabel = f"{question.replace('★ ', '')}"
        ylabel = f"{question2.replace('★ ', '')}"

        selected = ColumnDataSource(cross_tab)

        display_options = {
            "x_range": x_range,
            "y_range": y_range,
            "xlabel": xlabel,
            "ylabel": ylabel,
            "title": title,
            "tooltips": tooltips,
        }

        return selected, display_options, marker_scale

    def select_data_wordcloud(self, data_filters, data_filters_method, content):
        """Filter data for wordcloud from data filters"""
        word_list = []

        method_include = []
        method_exclude = []
        methods_dict = HCS_MCsubquestions[FILTER_BY_2]
        method_keys = list(methods_dict.keys())
        for method in data_filters_method:
            for key in method_keys:
                if methods_dict[key] == method:
                    method_include.append(key)
                    method_exclude.append((key, [False]))

        if len(data_filters_method) == 0:
            method_include = method_keys
            method_exclude = []

        # Process content specification
        data_include = []
        if "dataGenMethodSpec_" in content:
            for i, method in enumerate(method_include):
                id_meth = method[-1]
                if id_meth == "r":  # From other
                    id_meth = i + 1
                data_include.append("dataGenMethodSpec_{}_1".format(id_meth))
                data_include.append("dataGenMethodSpec_{}_2".format(id_meth))
                data_include.append("dataGenMethodSpec_{}_3".format(id_meth))
        else:
            data_include = content
            
        # Filter dataframe
        df = filter_dataframe(
            self.survey_data,
            include=[FILTER_BY] + method_include + data_include,
            exclude=method_exclude,
            as_type="str",
        )
        
        # Filter by research areas
        exclude = []
        for field in RESEARCH_FIELDS:
            if field not in data_filters:
                exclude.append(field)
        if "All" in data_filters:
            exclude = []
        for area in exclude:
            df = df[df[FILTER_BY] != area]

        # Prepare word list
        word_list = []
        for method in data_include:
            w_list = [word for word in df[method] if str(word) != "nan"]
            word_list = word_list + w_list

        return word_list