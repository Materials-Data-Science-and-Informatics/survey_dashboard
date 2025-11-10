
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

DEPLOYMENT ARCHITECTURE:
========================
This application uses Panel's built-in server (via `panel serve`) rather than
traditional WSGI servers like Gunicorn. This is the CORRECT and RECOMMENDED
approach for Panel applications.

Why subprocess + `panel serve` instead of Gunicorn:
----------------------------------------------------
1. **WebSocket Support**: Panel apps require WebSocket connections for real-time
   interactivity. Panel is built on Bokeh Server which uses Tornado's WebSocket
   implementation. Standard WSGI servers like Gunicorn don't natively support
   WebSockets in the same way.

2. **State Management**: Panel/Bokeh Server manages application state and sessions
   in a specific way that requires Tornado's event loop. Gunicorn's worker model
   doesn't provide this.

3. **Bokeh Protocol**: The Bokeh Server protocol handles bidirectional communication
   between Python and JavaScript using a custom protocol over WebSockets. This is
   deeply integrated with Tornado.

4. **Official Recommendation**: The Panel documentation recommends using `panel serve`
   for production deployments. See: https://panel.holoviz.org/how_to/deployment/

5. **Built-in Production Features**: `panel serve` includes production-ready features:
   - Multi-process scaling via --num-procs
   - WebSocket origin validation via --allow-websocket-origin
   - Static file serving
   - Load balancing across worker processes

Alternative Approaches (Not Recommended):
-----------------------------------------
- **Gunicorn + Flask wrapper**: Possible but adds unnecessary complexity and
  requires careful configuration of worker types (gevent/eventlet)
- **Embedding Panel in ASGI**: Possible with Daphne/Uvicorn but adds overhead

For more details, see DEPLOYMENT.md in the project root.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_app():
    """Run the survey dashboard application using Panel serve.

    Supports both development and production modes via command-line arguments.

    Kubernetes Deployment Note:
    ---------------------------
    For Kubernetes deployments, each pod should run a single process (no --num-procs).
    Kubernetes handles scaling via pod replicas and load balancing via Services.

    Example production deployment:
        survey-dashboard --production --host 0.0.0.0 --port 5006

    Then scale in Kubernetes:
        kubectl scale deployment survey-dashboard --replicas=3
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
        "--index", "app",  # Serve app.py at the root of prefix instead of /app
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