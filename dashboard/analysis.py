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
This module contains some function to process survey data in certain way and 
prepare the data for visualization
"""
import math
import pandas as pd
from typing import List, Tuple

def calculate_crosstab(df: pd.DataFrame, data_key1: str, data_key2: str, id_vars: str=None, astype: str="int") -> pd.DataFrame:
    """Calulate the cross table for two keys in a given pandas data frame"""
    if id_vars is None:
        id_vars = data_key1

    cols = [data_key1, data_key2]

    df0 = df[cols].dropna(how = "all", subset = cols).astype("category")
    totals = dict(df0[data_key1].value_counts())

    df_crosstab = pd.crosstab(df[data_key1], df[data_key2],
                              margins = False).reset_index().melt(id_vars = [id_vars])
    
    # include total answers by career level in cross tab
    df_crosstab["total"] = df_crosstab[data_key1].map(totals).astype(astype)
    
    # calculate relative amount of answers by career level
    df_crosstab["percentage"] = (df_crosstab["value"] / df_crosstab["total"]) * 100
    
    return df_crosstab


def filter_dataframe(df: pd.DataFrame, include: list=None, exclude: List[Tuple[str, list]]=None, exclude_nan=True, as_type="category") -> pd.DataFrame:
    """
    Filter pandas dataframe

    example:
    ```
    to_exclude = ['Other', 'Undergraduate / Masters student', 'Director (of the institute)']
    df = filter_dataframe(surveydata, include=["careerLevel", "docStructured", "researchArea"], exclude=[("careerLevel", to_exclude)])
    ```
    """
    
    if include is not None:
        df = df[include].dropna(how = "all", subset = include).astype(as_type)
    
    for key, val in exclude:
        df = df.loc[~df[key].isin(val)]
    
    if exclude_nan:
        for key in df.keys():
            df = df.loc[~df[key].isna()]
    return df

def get_all_values(df: pd.DataFrame, key: str) -> dict:
    """
    Count all values of a given key in a data frame and 
    return these values in a dictionary sorted.
    """
    all_areas = df[key].value_counts()
    all_areas = all_areas.sort_index()
    data = {'All': all_areas.values, key:list(all_areas.keys())}
    return data

def prepare_data_research_field(df: pd.DataFrame, key:str, key2:str='researchArea', sort_as=None):# -> dict, list:
    """Creates a dict dictionary with data in the form needed by the plotting functions
    
    We prepare several outputs, i.e y_keys because they can have different length and one should be able to create a 
    ColumnDataSource by ColumnDataSource(data=data)
    :param df: [description]
    :type df: pd.DataFrame
    :param key: [description]
    :type key: str

    example:
    prepare_data_research_field(df, key=careerLevel)
        {'Cum. Sum': array([  0,   0, 130, 128, 148, 272,   0]),
         'careerLevel': ['Director (of the institute)',
          'Other',
          'PhD student',
          'Postdoc',
          'Principal Investigator',
          'Research associate',
          'Undergraduate / Masters student'],
         'researchArea': ['Engineering Science',
          'Physics',
          'Life Science',
          'Earth Science',
          'Chemistry',
          'Other',
          'Psychology',
          'Mathematics'],
         'Engineering Science': array([  0,   0,  47,  30,  52, 134,   0]),
         'Physics': array([ 0,  0, 33, 38, 39, 57,  0]),
         'Life Science': array([ 0,  0, 28, 29, 27, 33,  0]),
         'Earth Science': array([ 0,  0,  8, 11, 18, 32,  0]),
         'Chemistry': array([ 0,  0,  9, 12,  6,  4,  0]),
         'Other': array([0, 0, 1, 2, 3, 6, 0]),
         'Psychology': array([0, 0, 3, 2, 3, 2, 0]),
         'Mathematics': array([0, 0, 1, 4, 0, 4, 0])}

    """
    all_areas = df[key].value_counts()
    all_areas = all_areas.sort_index()
    research_areas = list(df[key2].value_counts().keys())
    data = {'Cum. Sum': all_areas.values, key:list(all_areas.keys()), 'x_value': list(all_areas.keys())}
    y_keys = ['Cum. Sum'] + research_areas
    for area in research_areas:
        area_counts = df[df[key2] == area][key].value_counts()
        area_counts = area_counts.sort_index()
        data[area] = area_counts.values
    
    return data, y_keys

'''
def prepare_data_research_field(df: pd.DataFrame, key:str):
    """AI is creating summary for prepare_data_researchfield

    :param df: [description]
    :type df: pd.DataFrame
    :param key: [description]
    :type key: str
    """
    all_areas = df[key].value_counts()
    all_areas = all_areas.sort_index()
    data = {'All': {'counts': all_areas.values, 'values': list(all_areas.keys())}}
    research_areas = list(df['researchArea'].value_counts().keys())
    for area in research_areas:
        area_counts = df[df["researchArea"] == area][key].value_counts()
        area_counts = area_counts.sort_index()
        data[area] = {'counts': area_counts.values, 'values': list(area_counts.keys())}
    
    return data
'''

def percentage_to_area(data: List[float], scale_m: float=1.0) -> List[float]:
    """
    Convert numbers in a given array to a radius, 
    
    where a circle of with that radius is proportionate to the circle area 
    Useful for circle plots where the area should be proportional to the value
    """
    radius_data = [2*math.sqrt(val*scale_m/math.pi) for val in data]
    return radius_data