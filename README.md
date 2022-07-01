# Sterni_Puzzle
Python webserver for searching Sternburg crown caps for a puzzle/collection promotion. Images are taken from the official website: https://sternburg-bier.de/kronkorkenpuzzle

# Usage

pip install -r requirements.txt


(prepare images and download wheights on first run)

python offline.py


(run server on Powershell in local network)

$env:FLASK_APP = "server.py"

python -m flask run --host=0.0.0.0
