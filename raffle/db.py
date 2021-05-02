import pymongo
from flask import g

def get_db():

    # mongodb cluster is hosted on atlas, thus can be assessible from any where
    g.client = pymongo.MongoClient(
        "mongodb+srv://raffle_it:raffle_it@cluster0.qibte.mongodb.net/test?retryWrites=true&w=majority")
    db = g.client.test
    return db

def close_db(e=None):

    db = g.pop('client', None)
    
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)