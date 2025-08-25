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
    
    from service.api_gateway.main import SETTINGS

    uvicorn.run("service.api_gateway.main:create_app", host=SETTINGS.server,
                port=SETTINGS.app_port, workers=SETTINGS.workers,
                reload=SETTINGS.reload, factory=True, timeout_keep_alive=9000)
