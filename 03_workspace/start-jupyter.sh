#!/bin/bash
terminal -e ~/anaconda3/bin/jupyter lab --NotebookApp.iopub_data_rate_limit=1.0e10
xdg-open http://localhost:8888/