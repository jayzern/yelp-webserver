"""
Created on 3 Nov 2019
@author: Jay Zern Ng, Amaury Sudrie

Put Yelp database related things here only.

Note: Cannot use ORMs in sqlalchemy.
"""

import os
import psycopg2

from sqlalchemy import *
from sqlalchemy.pool import NullPool
from sqlalchemy import text
from sqlalchemy import exc

# sqlalchemy config
#DATABASEURI = "postgresql://jn2717:amaurylovesalex@34.74.165.156/proj1part2"
DATABASEURI = "postgresql://postgres:amaurylovesalex@127.0.0.1"

# psycopg2 config
#CONFIG = "host=34.74.165.156 \
#          dbname=proj1part2 \
#          user=jn2717 \
#          password=amaurylovesalex"
CONFIG = "dbname=postgres \
          user=postgres \
          password=amaurylovesalex"


def create_schema():
    """Create schema directly from yelp_schema.sql"""
    engine = create_engine(DATABASEURI)
    #schema_dir = os.path.join("./schema", "yelp_schema.sql")
    schema_dir = os.path.join("./schema", "yelp_schema_Project2.sql")
    schema_file = open(schema_dir)
    sql_command = text(schema_file.read())
    try:
        engine.execute(sql_command)
    except exc.SQLAlchemyError:
        raise

def tabulate_friends():
    engine = create_engine(DATABASEURI)
    sql_command = """INSERT INTO Friend_Of
                        (friendship_id,
                         user_one_id,
                         user_two_id)
                     VALUES ('1','1','2'),('2','2','5'),('3','3','4'),('4','5','10'),('5','2','10'),('6','23','21'),('7','20','14'),('8','15','17'),('9','20','1'),('10','1','3'),
                            ('11','1','4'),('12','1','5'),('13','1','6'),('14','1','7'),('15','1','8'),('16','1','9'),('17','1','10'),('18','1','11'),('19','1','12'),('20','1','13'),
                            ('21','1','14'),('22','1','15'),('23','1','16'),('24','1','17'),('25','1','18');
                  """
    try:
        engine.execute(sql_command)
    except exc.SQLAlchemyError:
        raise

def tabulate_business(data):
    """
    Use psycopg2 instead of sqlalchemy to tabulate data. Not allowed to use
    ORM, so the goal is to use mogrify to prepare large insert statements.
    """
    try:
        conn = psycopg2.connect(CONFIG)
        cur = conn.cursor()
        args_str = ','.join(
            cur.mogrify(
                """(%s,%s,%s,%s,%s,%s,%s,%s,%s,ROW(%s,%s,%s,%s),%s,ROW(%s,%s,%s,%s,%s,%s,%s))""",
                x).decode("utf-8") for x in data)
        sql_command = """INSERT INTO Business
                            (business_id,
                            name,
                            address,
                            city,
                            state,
                            postal_code,
                            review_count,
                            categories_list,
                            avg_stars,
                            attribute,
                            price_range,
                            open_hours)
                        VALUES """ + args_str + ";"

        # sql_command = """INSERT INTO Business
        #                     (business_id,
        #                     name,
        #                     address,
        #                     city,
        #                     state,
        #                     postal_code,
        #                     review_count,
        #                     categories_list,
        #                     avg_stars,
        #                     to_go,
        #                     wifi,
        #                     ambience,
        #                     parking,
        #                     price_range,
        #                     open_hours)
        #                 VALUES """ + args_str + ";"
        cur.execute(sql_command)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def tabulate_yelp_user(data):
    try:
        conn = psycopg2.connect(CONFIG)
        cur = conn.cursor()
        args_str = ','.join(cur.mogrify(
            "(%s,%s,%s,%s,%s,%s)", x).decode("utf-8") for x in data)
        sql_command = """INSERT INTO Yelp_User
                            (user_id,
                            name,
                            registration_date,
                            fans,
                            avg_stars,
                            review_count)
                        VALUES """ + args_str + ";"
        cur.execute(sql_command)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def tabulate_reviews(data):
    try:
        conn = psycopg2.connect(CONFIG)
        cur = conn.cursor()
        args_str = ','.join(cur.mogrify(
            "(%s,%s,%s,%s,%s,%s,%s,%s)", x).decode("utf-8") for x in data)
        sql_command = """INSERT INTO Reviews
                            (review_id,
                            business_id,
                            user_id,
                            review_date,
                            stars,
                            review_text,
                            review_text_tsvector,
                            useful_count)
                        VALUES """ + args_str + ";"
        cur.execute(sql_command)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def tabulate_tips(data):
    try:
        conn = psycopg2.connect(CONFIG)
        cur = conn.cursor()
        args_str = ','.join(cur.mogrify(
            "(%s,%s,%s,%s,%s,%s)", x).decode("utf-8") for x in data)
        sql_command = """INSERT INTO Tips
                            (business_id,
                            user_id,
                            compliment_count,
                            tip_date,
                            tip_text,
                            tip_text_tsvector)
                        VALUES """ + args_str + ";"
        cur.execute(sql_command)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def tabulate_checkins(data):
    try:
        conn = psycopg2.connect(CONFIG)
        cur = conn.cursor()
        args_str = ','.join(cur.mogrify(
            "(%s,%s)", x).decode("utf-8") for x in data)
        sql_command = """INSERT INTO Checkins
                            (business_id,
                            checkin_date)
                        VALUES """ + args_str + ";"
        cur.execute(sql_command)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def tabulate_media(data):
    try:
        conn = psycopg2.connect(CONFIG)
        cur = conn.cursor()
        args_str = ','.join(cur.mogrify(
            "(%s,%s,%s,%s)", x).decode("utf-8") for x in data)
        sql_command = """INSERT INTO Media
                            (photo_id,
                            business_id,
                            blob_data,
                            caption)
                        VALUES """ + args_str + ";"
        cur.execute(sql_command)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
