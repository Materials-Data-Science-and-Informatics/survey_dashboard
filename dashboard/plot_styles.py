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
This contains external style definitions, specific for the HMC dashboard

This can either be apllied to figures after bokeh plots, or some can be profided to the ploting function
as figure_kwargs, but only kwargs taken by the figure constructor
"""

from bokeh.models import figure as bokeh_figure


FIGURE_WIDTH = 900
FIGURE_HEIGHT = 600

def hmc_barchart_pre_style(changes:dict = {})-> dict :
    
    figure_kwargs_defaults = {}
    # maybe do a rekursive merge here
    figure_kwargs = figure_kwargs_defaults.update(changes)

    return figure_kwargs

def hmc_barchart_post_style(fig: bokeh.models.figure) -> dict:
    """
    Define some figure properties for HMC dashboard barcharts
    """ 

    # todo figure out a way how to apply the dot notation from a given dict...
    # The last value can be set in bokeh with 'set_from_json', it is still unclear to me
    # how one can get the

    fig.x_range.range_padding = 0.1
    fig.xgrid.grid_line_color = None
    fig.legend.location = "top_left"
    fig.legend.orientation = "horizontal"
    fig.y_range.start = 0
    fig.xaxis.major_label_orientation = 1
    fig.yaxis.axis_label = ylabel
    fig.xaxis.axis_label = xlabel
    fig.title.text_font_size='25px'
    fig.yaxis.axis_label_text_font_size = '22px'
    fig.xaxis.axis_label_text_font_size = '22px'
    fig.xaxis.major_label_text_font_size = '18px'
    fig.xaxis.major_label_text_font_size = '18px'
    fig.toolbar.logo = None
    fig.legend.location = "top_right"
    fig.legend.orientation = "vertical"
    fig.legend.click_policy="hide"
    


    return fig



def hmc_pie_pre_style(changes:dict = {}) -> dict:
    """
    Define some figure properties for HMC dashboard piecharts
    """

    figure_kwargs_defaults = {}
    
    # maybe do a rekursive merge here
    figure_kwargs = figure_kwargs_defaults.update(changes)
    

    return figure_kwargs


def hmc_corr_pre_style(changes:dict = {}) -> dict:
    """
    Define some figure properties for HMC dashboard correlation charts
    """
    figure_kwargs_defaults = {}
    
    # maybe do a rekursive merge here
    figure_kwargs = figure_kwargs_defaults.update(changes)
    

    return figure_kwargs