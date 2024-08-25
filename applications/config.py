from datetime import timedelta
import os

appdir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG=True
    #Setting permanent session lifetime to 1 day.
    SQLITE_DB_DIR=os.path.join(appdir,"..")
    PERMANENT_SESSION_LIFETIME= timedelta(days=1)
    SECRET_KEY='developmentProject23'
    SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(SQLITE_DB_DIR,'eventease.sqlite3')

    