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
This file contains color palettes which are HMC specific
@author: s.gerlich
"""

from typing import Optional, List, Any

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

# Create color ramps for continuous data out of color palettes
def make_Ramp(ramp_colors: List[str]) -> Optional[Any]:
    """Create a matplotlib colormap from a list of colors."""
    try:
        from colour import Color  # type: ignore[import-untyped]
        from matplotlib.colors import LinearSegmentedColormap  # type: ignore[import-untyped]
        color_ramp = LinearSegmentedColormap.from_list('hmc_colormap', [Color(c1).rgb for c1 in ramp_colors])
        return color_ramp
    except ImportError:
        # Fallback if optional dependencies aren't available
        return None


# Create color ramps (only if dependencies are available)
HMCRamp = make_Ramp(HMCPalette)
hubInfoRamp = make_Ramp(hubInfoPalette)

# Generate HMC color samples for Bokeh (fallback to basic colors if dependencies fail)
def get_hmc_colors(n_colors: int = 10) -> List[str]:
    """Get n_colors from the HMC palette, cycling if needed."""
    if len(HMCPalette) >= n_colors:
        return HMCPalette[:n_colors]
    else:
        # Cycle through colors if we need more than available
        return [HMCPalette[i % len(HMCPalette)] for i in range(n_colors)]
