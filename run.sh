#!/bin/bash
python3 -m pip install --upgrade pip
pip3 install virtualenv
mkdir -p venv
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
pyinstaller --onefile --windowed -i sweeper.ico -n CrownSweeper sweeper.py 
