"""
USAGE: python3 run_server.py --service [name of service]

                       NOTE:
                       ----
Before running the server make sure you have following environment
variables available

ENVIRONMENT
PYTHONPATH
"""

import os
import sys
from pathlib import Path

import uvicorn
import argparse

import logging
    
if __name__ == "__main__":
    """
    * Initialize logger
    * Runs the app
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--service", required=True) 
    args = parser.parse_args()

    os.environ["SERVICE"] = args.service
    
    # Add your module directory to sys.path
    current_path = Path.cwd()
    
    module_path = str(current_path.parents[1])
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

    from service.api_gateway.main import SETTINGS

    uvicorn.run("service.api_gateway.main:create_app", host=SETTINGS.server,
                port=SETTINGS.app_port, workers=SETTINGS.workers,
                reload=SETTINGS.reload, factory=True, timeout_keep_alive=9000)
