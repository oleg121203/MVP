#!/bin/bash

# Set Python path
export PYTHONPATH="/Users/olegkizyma/workspaces/MVP/ventai-app:$PYTHONPATH"

# Run tests
pytest backend/tests/test_analytics_api.py
