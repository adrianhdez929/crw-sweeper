#!/bin/bash
mkdir venv
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
pyinstaller --onefile --icon=sweeper.ico -n CrownSweeper sweeper.py 
