import os
import dotenv

dotenv.load_dotenv(".flaskenv")

# flask
ENV = os.environ.get("FLASK_ENV")
DEBUG = os.environ.get("FLASK_DEBUG")
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
# postgres
DB_USER = "postgres"
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = "localhost"
DATABASE = "trivia"
DB_PORT = 5432

# sql alchemy
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
