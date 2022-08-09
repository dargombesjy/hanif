import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(1, '/home/warno006089/.pyenv/versions/')

from main import create_app

application = create_app()