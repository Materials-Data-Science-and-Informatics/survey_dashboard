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
import requests
# HMC survey data:
#doi = 'https://doi.org/10.7802/2433'
#https://search.gesis.org/research_data/SDN-10.7802-2433?doi=10.7802/2433
#url="https://access.gesis.org/sharing/2433/3778"

def download_data(url="https://access.gesis.org/sharing/2433/3778", 
    destination="survey_dashboard/data/hmc_survey_2021_data_cleaned.csv"):
    """
    This function downloads the dataset for a given DOI
    """
    # For now go to the website of the DOI and download by hand

    with open(destination, "wb") as fileo:
        fileo.write(requests.get(url).content)

