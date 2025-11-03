
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

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_app():
    """Run the survey dashboard application using Panel serve.

    Supports both development and production modes via command-line arguments.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run the HMC Survey Dashboard")
    parser.add_argument(
        "--production",
        action="store_true",
        help="Run in production mode (for Docker/server deployments)"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host to bind to (default: localhost, use 0.0.0.0 for production)"
    )
    parser.add_argument(
        "--port",
        default="5006",
        help="Port to run the server on (default: 5006)"
    )
    args = parser.parse_args()

    # Read URL prefix from environment (set by Docker Compose VIRTUAL_PATH)
    # This is needed when the dashboard is served from a subpath (e.g., /2021community)
    virtual_path = os.environ.get("VIRTUAL_PATH", "").strip()

    # Get the directory containing app.py (same directory as scripts.py)
    script_dir = Path(__file__).parent
    app_path = script_dir / "app.py"

    # Static files directory for assets
    static_dir = script_dir / "hmc_layout" / "static" / "en_files"

    # Build the panel serve command
    cmd = [
        sys.executable, "-m", "panel", "serve",
        str(app_path),
        "--port", args.port,
        "--address", args.host if args.production else "localhost",
        "--static-dirs", f"en_files={static_dir}",
    ]

    # Production-specific settings
    if args.production:
        cmd.extend([
            "--allow-websocket-origin", "*",  # Allow external connections
        ])
        print("Starting HMC Survey Dashboard in PRODUCTION mode...")
        print(f"Server will be accessible at http://{args.host}:{args.port}")
    else:
        # Development mode - open browser automatically
        cmd.append("--show")
        print("Starting HMC Survey Dashboard in DEVELOPMENT mode...")

    # Add URL prefix if VIRTUAL_PATH is set (for serving from subpath)
    # This tells Panel to prepend the path to all generated URLs (static files, WebSockets, etc.)
    if virtual_path:
        cmd.extend(["--prefix", virtual_path])
        print(f"Using URL prefix: {virtual_path}")
        if args.production:
            print(f"Dashboard will be accessible at: http://{args.host}:{args.port}{virtual_path}")

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