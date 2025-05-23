#!/usr/bin/env bash
cd "$(dirname "$0")"
source venv/bin/activate
python get_data.py
python generate_summary.py