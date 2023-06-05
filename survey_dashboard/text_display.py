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
This is the central place for all text from the dashboard which needs to be translated
"""


# Description
md_text_description = {'EN': ("Explorer interactively the HMC 2021 Survey results. "
    "The overview sections displays some main results, while you can apply some global filters to these. " 
    "Find out what methods, tools, software and standards are applied by others in your research area. "
    "The question explorer allows for in detail analysis of a specific question and simple correlations of two questions. "
    "Interact with the visualizations and widgets on the left to explorer the data.\n"
    "The corresponding Data publication of the survey is available [here](https://doi.org/10.7802/2433).\n"
    "\n "
    "DISCLAIMER: Be careful in drawing any conclusions, especially on filtered results! "
    "The usable sample size of the survey 2021 was 2.3% of all Helmholtz employees at the time, of "# <3
    "which only the onces are published and displayed who provided consent. "
    "Therefore, the sample is often to small to be an accurate representation of the whole HGF "
    "and or to unbiased accurately sample the underlying true distributions!\n"
    "\n"
    "Any Feedback is welcome and can be given [here](https://github.com/Materials-Data-Science-and-Informatics/survey_dashboard)"),
    'DE':('Exploriere interakiv die Resultate der HMC 2021 Umfrage.')}



## Global data filters\n 
md_text_global_filter = {'EN': ("Apply filters to displayed data according to research areas and data generation method"),
                         'DE': ("Wende Filter auf die Resultate an um nur Daten bestimmter "
                         "Forschungsfelder und Erzeugungsmethode dazustellen.")}

md_text_global_filters_widgets = [{'EN': "Research area", 'DE': "Forschungsfeld"}, {'EN': "Data generation method", 'DE': "Datenerzeugungs Methode"}]

# Overview\n
md_text_overview = {'EN': "Birds eye view of survey results related to research data management.",
                    'DE': "Übersicht mit hervorgehobene Fragen zum Forschungsdatenmanagement"}




# Tools and Methods\n 
md_text_tools_used = {'EN': ("Discover the scientific methods, used software and repositories of our communities."),
                    'DE': ("Entdecke die wissenschaftliche Methoden, Werkzeuge, Software und Repositorien welche in unseren Forschungsgemeinschaft "
                    "genutzt werden.")}

# Question explorer

md_text_barchart = {'EN': ("Select two questions to explore answers and see how they correspond to one another."),
                    'DE': ("Wähle zwei Fragen aus um deren Anworten zu sehen und wie diese übereinstimmen.")}

md_text_select_widgets = [{'EN': "Question 1", 'DE': "Frage 1"}, {'EN': "Question 2", 'DE': "Frage 2"}]
# Basic Correlations\n
md_text_corrchart = {'EN': "Correspondence of selected questions",
                    'DE': "Korrespondenz der ausgewählten Fragen"}

md_text_button = {'EN': ("# Further charts\n")}

accordion_titles = {
    'EN': ['Global Data Filters', 'Overview', 'Methods, Tools and Software', 'Survey Data Explorer'],
    'DE': ['Globale Datenfilter', 'Überblick', 'Methoden, Werkzeuge und Software', 'Umfrage-explorer']
}