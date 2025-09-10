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
Command line scripts for the survey dashboard.
"""

import subprocess
import sys
from pathlib import Path


def run_app():
    """Run the survey dashboard application using Panel serve."""
    # Get the directory containing app.py (project root)
    project_root = Path(__file__).parent.parent
    app_path = project_root / "app.py"
    
    # Static files directory for assets
    static_dir = project_root / "survey_dashboard" / "hmc_layout" / "static" / "en_files"
    
    # Build the panel serve command
    cmd = [
        sys.executable, "-m", "panel", "serve",
        str(app_path),
        "--port", "5006",
        "--static-dirs", f"en_files={static_dir}",
        "--show"
    ]
    
    print("Starting HMC Survey Dashboard...")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running dashboard: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
        sys.exit(0)


if __name__ == "__main__":
    run_app()