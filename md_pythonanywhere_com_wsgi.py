import sys
import os

# Chemin vers ton projet
path = '/home/MD/mon_projet1'
if path not in sys.path:
    sys.path.insert(0, path)

# Mode production
os.environ['FLASK_ENV'] = 'production'

# Import de ton application Flask
from app import app as application

