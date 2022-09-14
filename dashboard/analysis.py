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


def filter_dataframe(df: pd.DataFrame, include: list=None, exclude: List[Tuple[str, list]]=None, 
                exclude_nan=True, exclude_anonymized=True, as_type="category") -> pd.DataFrame:
    """
    Filter a pandas dataframe

    example:
    ```
    to_exclude = ['Other', 'Undergraduate / Masters student', 'Director (of the institute)']
    df = filter_dataframe(surveydata, include=["careerLevel", "docStructured", "researchArea"], exclude=[("careerLevel", to_exclude)])

    returns a dataFrame with columns ["careerLevel", "docStructured", "researchArea"], 
    where rows which contain to_exclude values in the "careerLevel" column are removed
    ```
    """


    if include is not None:
        df = df[include].dropna(how = "all", subset = include).astype(as_type)
    
    for key, val in exclude:
        #print(key, val)
        df = df.loc[~df[key].isin(val)]
    
    if exclude_nan:
        for key in df.keys():
            df = df.loc[~df[key].isna()]

    if exclude_anonymized:
        df = df.replace(to_replace="Anonymized", value="") 

    return df

def get_all_values(df: pd.DataFrame, keylist: List[str], display_dict=None) -> dict:
    """
    Count all values of a given key from a key list in a data frame and 
    return these values in a dictionary sorted.

    """
    if len(keylist) == 1:
        key = keylist[0]
        all_areas = df[key].value_counts()
        all_areas = all_areas.sort_index()
        data = {'All': all_areas.values, key:list(all_areas.keys())}
    else: # multiple keys now the keys become the xticks
        combined = {}
        for key in keylist:
            if display_dict is not None:
                xtick = display_dict[key]
            else:
                xtick = key
            xtick = xtick.replace(' \n', '')
            temp = df[key]
            temp.replace(to_replace=True, value=xtick, inplace=True)
            temp.replace(to_replace=False, value=None, inplace=True)
            a = temp.value_counts()
            if a.empty:
                combined[xtick] = 0
            else:
                # greedy, there is probably a pandas way to do this...
                # there is a problem if df is empty, i.e temp.value_counts() True 0
                for i, ke in enumerate(a.keys()):
                    # because other can contain all... others..
                    #ke = ke.lower() # sometimes there are mixed upper and lower case keys...
                    #ke = ke.replace(' \n', '') # some are with and without breaks
                    temp_val = combined.get(ke, 0)
                    temp_val = temp_val + a.values[i]
                    combined[ke] = temp_val

            #for i, ke in enumerate(a.keys()):
            #    ke = ke.lower() # sometimes there are mixed upper and lower case keys...
            #    ke = ke.replace(' \n', '') # some are with and without breaks
            #    temp_val = combined.get(ke, 0)
            #    temp_val = temp_val + a.values[i]
            #    combined[ke] = temp_val
        data = {'All' : list(combined.values()), key:list(combined.keys())}
    return data


def prepare_data_research_field(df: pd.DataFrame, keylist:List[str], key2:str='researchArea', sort_as=None, display_dict= None):# -> dict, list:
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
    research_areas = list(df[key2].value_counts().keys())
    y_keys = ['Cum. Sum'] + research_areas
    # Multiple columns will be combined. A single column will be treated differently
    if len(keylist) == 1:
        key = keylist[0]
        all_areas = df[key].value_counts()
        all_areas = all_areas.sort_index()
        data = {'Cum. Sum': all_areas.values, key:list(all_areas.keys()), 'x_value': list(all_areas.keys())}
        for area in research_areas:
            area_counts = df[df[key2] == area][key].value_counts()
            area_counts = area_counts.sort_index()
            data[area] = area_counts.values
    else:
        # Cum. Sum. is buggy?
        combined = {}
        data = {}
        for key in keylist:
            if display_dict is not None:
                xtick = display_dict[key]
            else:
                xtick = key
            xtick = xtick.replace(' \n', '')
            temp = df[key]
            temp.replace(to_replace=True, value=xtick, inplace=True)
            temp.replace(to_replace=False, value=None, inplace=True)
            a = temp.value_counts()
            # greedy, there is probably a pandas way to do this...
            # there is a problem if df is empty, i.e temp.value_counts() True 0
            if a.empty:
                combined[xtick] = 0
            else:  
                for i, ke in enumerate(a.keys()):
                    # because other can contain all... others..
                    #ke = ke.lower() # sometimes there are mixed upper and lower case keys...
                    #ke = ke.replace(' \n', '') # some are with and without breaks
                    temp_val = combined.get(ke, 0)
                    temp_val = temp_val + a.values[i]
                    combined[ke] = temp_val
            
            # now fill research area specifics
            for area in research_areas:
                area_counts = df[df[key2] == area][key]
                area_counts.replace(to_replace=True, value=xtick, inplace=True)
                area_counts.replace(to_replace=False, value=None, inplace=True)
                area_counts = area_counts.value_counts()
                area_counts = area_counts.sort_index()
                temp = data.get(area, [])
                #print(area_counts)
                if area_counts.empty:
                    temp.append(0)
                else:
                    temp.append(int(area_counts.values[0]))
                data[area] = temp
        
        data['Cum. Sum'] = list(combined.values())
        data['x_value'] = list(combined.keys())

    return data, y_keys

'''
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