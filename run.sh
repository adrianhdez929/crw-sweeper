#!/bin/bash
mkdir venv
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
pyinstaller --onefile main.py
