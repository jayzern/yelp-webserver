"""
Created on 3 Nov 2019
@author: Jay Zern Ng, Amaury Sudrie

Put Yelp database related things here only.

Note: Cannot use ORMs in sqlalchemy.
"""

import utility as util
import os
import psycopg2

from sqlalchemy import *
from sqlalchemy.pool import NullPool
from sqlalchemy import text
from sqlalchemy import exc

"""Test only"""

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


def tabulate_business(blist):
    """
    Use psycopg2 instead of sqlalchemy to tabulate data. Not allowed to use
    ORM, so the goal is to use mogrify to prepare large insert statements.
    """
    try:
        conn = psycopg2.connect(
            "dbname=postgres \
            user=postgres \
            password=amaurylovesalex"
        )
        cur = conn.cursor()

        args_str = ','.join(cur.mogrify(
            "(%s,%s,%s,%s,%s,%s,%s,%s,%s)", x).decode("utf-8") for x in blist)

        sql_command = """INSERT INTO business
                            (business_id,
                            name,
                            address,
                            city,
                            state,
                            postal_code,
                            review_count,
                            categories_list,
                            avg_stars)
                        VALUES """ + args_str + ";"

        cur.execute(sql_command)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


test_list = util.get_business_list()
key_list = ['business_id', 'name', 'address', 'city', 'state',
            'postal_code', 'review_count', 'categories', 'stars']
test_list = util.parse_dict_to_list(key_list, test_list)

tabulate_business(test_list)
