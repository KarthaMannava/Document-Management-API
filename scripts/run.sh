#!/bin/bash
# Make sure to give the scripts executable permissions if running on a Unix-like system. You can do this by running chmod +x run.sh in the terminal.
poetry run uvicorn main:app --reload