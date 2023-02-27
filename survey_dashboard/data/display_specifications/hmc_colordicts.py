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
This file contains color palets which are HMC specific
@author: s.gerlich
"""

import matplotlib.pyplot as plt
import cmasher as cmr
colors = cmr.take_cmap_colors(HMCRamp, None, cmap_range=(0.2, 0.8), return_fmt='hex')



# Dictionary of HMC hub colors                         
hubPalette = {
        "Information":"#A0235A",
        "Health":"#D23264",
        "Matter":"#F0781E",
        "Energy":"#FFD228",
        "Aeronautics, Space and Transport":"#50C8AA",
        "Earth and Environment":"#326469"
        }

# List of HMC color palette
HMCPalette = [
        "#A3C6E1",
        "#005AA0",
        "#0A2D6E",
        "#1B3142",
        "#5A696E",
        "#7B878B",
        "#ADB7BA",
        "#D6F094",
        "#8CB423",
        "#3F5704"
        ]

# List of Hub Info color Palette        
hubInfoPalette = [
        "#005AA0",
        "#0A2D6E",
        "#051E30",
        "#454747",
        "#7B878B",
        "#D979A3",
        "#A0235A",
        "#5E2940",
        "#470723"
        ]

# create color ramps for continuous data out of color palettes
# function to create ramp: make_ramp()
def make_Ramp( ramp_colors ): 
    from colour import Color
    from matplotlib.colors import LinearSegmentedColormap

    color_ramp = LinearSegmentedColormap.from_list( 'my_list', [ Color( c1 ).rgb for c1 in ramp_colors ] )
    plt.figure( figsize = (15,3))
    plt.imshow( [list(np.arange(0, len( ramp_colors ) , 0.1)) ] , interpolation='nearest', origin='lower', cmap= color_ramp )
    plt.xticks([])
    plt.yticks([])
    return color_ramp


# to be used in matplotlib: cmap
# equivalent of plotnine: scale_color_cmap()
# continuous color scale based on HMC color palette
HMCRamp = make_Ramp(HMCPalette)
#cmr.view_cmap(HMCRamp)

# continuous color scale based on Hub Info color palette
hubInfoRamp = make_Ramp(hubInfoPalette)
#cmr.view_cmap(hubInfoRamp)


