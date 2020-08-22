import os

cwd = os.path.abspath(os.getcwd())
db_path = os.path.join(cwd, 'data.db')


class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "*ER^F&D3928dhe298V@EYYIE@GU3928dhe298*IYEG"
    STATIC_FOLDER = "public"
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_ACCEPT_CONTENT = ['pickle', 'json']
