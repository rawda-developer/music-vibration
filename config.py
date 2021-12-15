from dotenv import load_dotenv
import os
from os import getenv
SECRET_KEY = getenv('SECRET_KEY', None)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


load_dotenv()

SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', None)
