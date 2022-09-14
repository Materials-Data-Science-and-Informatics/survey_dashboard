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
    "The overview sections displays some main results, while you can apply some global filters to these." 
    "Find out what methods, tools, software and standards are applied by others in your research are. "
    "The question explorer allows you do in detail analyze a specific question. "
    "Interact with the visualizations and widgets on the left to explorer the data.\n"
    "The corresponding Data publication of the survey is available [here](https://doi.org/10.7802/2433).\n"
    "\n "
    "DISCLAIMER: Be careful in drawing any conclusions, especially on filtered results! "
    "The usable sample size of the survey 2021 was 2.3% of all Helmholtz employees at the time "# <3
    "and therefore is often two small to be an accurate representation of the whole HGF "
    "and or to unbiased accurately sample the underlying true distributions!"),
    'DE':('Exploriere interakiv die Resultate der HMC 2021 Umfrage.')}



## Global data filters\n 
md_text_global_filter = {'EN': ("Select some data filters to apply. "
                         "You can filter global by research area and or by data generation method."),
                         'DE': ("Wähle Datenfilter aus. Die Resultate können global nach "
                         "Forschungsfeld und Erzeugungsmethode gefiltert werden.")}
# Overview\n
md_text_barchart = {'EN': ("Use this area to explorer the results for each survey question. "
                    "Use the dropdown menus to select the question of interest."),
                    'DE': ("Exploriere hier die Resultate für den Teil der Umfrage welcher dich am meisten interessiert. "
                    "Benutze die Auswahlwidgets um die Resultate einer bestimmten Frage anzuzeigen.")}
# Basic Correlations\n
md_text_corrchart = {'EN': ("Find out about basic correlation of answers, "
                    "i.e. how many participants provided the same answer two questions."),
                    'DE': ("Finde heraus wie Antworten zweier Fragen sich überschneiden. "
                    "Also wie viele der Befragten gleich auf zwei Fragen geantwortet haben.")}

md_text_button = {'EN': ("# Further charts\n")}

# Tools and Methods\n 
md_text_tools_used = {'EN': ("Find out about the tools and methods used in the "
                    "research area and data generation method you filtered for."),
                    'DE': ("Finde heraus welche Methoden, welche Werkzeuge und welche Software "
                    "in welchem Anwendungsbereich genutzt wird.")}



accordion_titles = {
    'EN': ['Global Data Filters', 'Overview', 'Methods, Tools and Software', 'Survey Data Explorer'],
    'DE': ['Globale Datenfilter', 'Überblick', 'Methoden, Werkzeuge und Software', 'Umfrage-explorer']
}