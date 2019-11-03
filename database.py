"""
Created on 3 Nov 2019
@author: Jay Zern Ng, Amaury Sudrie

Put Yelp database related things here only.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from sqlalchemy import text
from sqlalchemy import exc

# Local Database
DATABASEURI = "postgresql://postgres:amaurylovesalex@127.0.0.1"

def create_schema():
    """Create schema directly from yelp_schema.sql"""
    engine = create_engine(DATABASEURI)
    schema_dir = os.path.join("./schema", "yelp_schema.sql")
    schema_file = open(schema_dir)
    sql_command = text(schema_file.read())

    try:
        engine.execute(sql_command)
    except exc.SQLAlchemyError:
        raise
