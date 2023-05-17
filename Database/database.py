import os
import datetime
from pony.orm import *

def define_entities(
    db: Database
    ) -> None:

    class Competition(db.Entity):
        code     = PrimaryKey(str)
        name     = Required(str)
        areaName = Required(str)
        teams    = Set('Team')
        coaches  = Set('Coach')


    class Team(db.Entity):
        id           = PrimaryKey(int, auto = True)
        name         = Required(str, unique = True)
        shortName    = Optional(str)
        tla          = Required(str)
        areaName     = Required(str)
        address      = Required(str)
        coaches      = Set('Coach')
        players      = Set('Player')
        competitions = Set('Competition')


    class Player(db.Entity):
        id          = PrimaryKey(int, auto = True)
        name        = Required(str)
        position    = Optional(str)
        dateOfBirth = Optional(datetime.date)
        nationality = Optional(str)
        team        = Required ('Team')


    class Coach(db.Entity):
        id              = PrimaryKey(int, auto = True)
        name            = Optional(str)
        dateOfBirth     = Optional(datetime.date)
        nationality     = Optional(str)
        team            = Set ('Team')
        competitions    = Set('Competition')


def setup_db(filepath = None):
    db = Database()
    if filepath and not os.path.exists(filepath):
        db.bind(provider='sqlite', filename=filepath, create_db=True)
    else:
        db.bind(provider='sqlite', filename=':memory:', create_db=True)
    define_entities(db)
    db.generate_mapping(create_tables=True)

    return db

db = setup_db("football.sqlite")
