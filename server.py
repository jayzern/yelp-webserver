#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.

NOTE: Remember to handle SQL Injections, otherwise lose marks
"""

import os
import utility as util
import database as db
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response


tmpl_dir = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)),
    'templates')
app = Flask(__name__, template_folder=tmpl_dir)

"""Google Cloud database"""
#DATABASEURI = "postgresql://jn2717:amaurylovesalex@35.196.44.144/w4111"
DATABASEURI = "postgresql://postgres:amaurylovesalex@127.0.0.1"

engine = create_engine(DATABASEURI)

# Tabulates data using database.py and utility.py
db.create_schema()
business_data = util.get_business()
db.tabulate_business(business_data)
yelp_user_data = util.get_yelp_user()
db.tabulate_yelp_user(yelp_user_data)
reviews_data = util.get_reviews()
db.tabulate_reviews(reviews_data)
tips_data = util.get_tips()
db.tabulate_tips(tips_data)
checkins_data = util.get_checkins()
db.tabulate_checkins(checkins_data)
media_data = util.get_media()
db.tabulate_media(media_data)


@app.before_request
def before_request():
    """
    This function is run at the beginning of every web request
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request.

    The variable g is globally accessible.
    """
    try:
        g.conn = engine.connect()
    except BaseException:
        print "uh oh, problem connecting to database"
        import traceback
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass


@app.route('/')
def index():
    """
    request is a special object that Flask provides to access web request information:

    request.method:   "GET" or "POST"
    request.form:     if the browser submitted a form, this contains the data in the form
    request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

    See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
    """

    # For debugging
    print request.args

    cursor = g.conn.execute("SELECT * FROM business")
    names = []
    for result in cursor:
        names.append(result)
    cursor.close()
    context = dict(data=names)

    return render_template("index.html", **context)


@app.route('/another')
def another():
    return render_template("another.html")


@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
    return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


# TODO: implement
@app.route('/get_business', methods=['POST'])
def get_business():
    business = request.form['business']
    cursor = g.conn.execute('SELECT * FROM Business WHERE business_id = %s',(business))
    names = []
    for result in cursor:
        names.append(result['name'])
    cursor.close()
    context = dict(data=names)
    return render_template("index.html", **context)

# TODO: implement
# @app.route('/get_yelp_user', methods=['POST'])
# def get_yelp_user():
#     pass
#
# # TODO: implement
# @app.route('/get_reviews', methods=['POST'])
# def get_yelp_user():
#     pass
#
# # TODO: implement
# @app.route('/get_tips', methods=['POST'])
# def get_yelp_user():
#     pass
#
# # TODO: implement
# @app.route('/get_yelp_user', methods=['POST'])
# def get_yelp_user():
#     pass

if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using:

            python server.py

        Show the help text using:

            python server.py --help

        """

        HOST, PORT = host, port
        print "running on %s:%d" % (HOST, PORT)
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()
