ECHO OFF
ECHO "INSTALLING REQUIREMENTS..."
pip install --user -r requirements.txt
ECHO "STARTING APPLICATION..."
python main.py
ECHO "APPLICATION CLOSED"