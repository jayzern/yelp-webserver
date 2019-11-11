#!/usr/bin/env python3.6

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.

NOTE:
- Remember to handle SQL Injections, otherwise lose marks
- Should be able to DELETE
- Implement ERROR handling
"""

import os
import psycopg2
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
        print("uh oh, problem connecting to database")
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
    print(request.args)

    return render_template("index.html")


@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
    return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


"""Basic Queries"""
@app.route('/get_business', methods=['POST'])
def get_business():
    # Get data from forms
    business_id = request.form['business_id']
    name = request.form['name']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']

    # Execute query
    cursor = g.conn.execute(
        'SELECT * FROM Business WHERE \
            (business_id = %s OR name = %s OR \
            address = %s OR city = %s OR state = %s)',
        (business_id, name, address, city, state)
    )

    # Fetch data
    data = []
    for result in cursor:
        data.append({
            'business_id':result['business_id'],
            'name':result['name'],
            'address':result['address'],
            'city':result['city'],
            'state':result['state'],
            'postal_code':result['postal_code'],
            'review_count':result['review_count'],
            'categories_list':result['categories_list'],
            'avg_stars':result['avg_stars'],
            'to_go':result['to_go'],
            'wifi':result['wifi'],
            'ambience':result['ambience'],
            'parking':result['parking'],
            'price_range':result['price_range'],
            'open_hours':result['open_hours']
        })
    cursor.close()

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/get_yelp_user', methods=['POST'])
def get_yelp_user():
    # Get data from forms
    user_id = request.form['user_id']
    name = request.form['name']

    # Execute query
    cursor = g.conn.execute(
        'SELECT * FROM Yelp_User WHERE \
            (user_id = %s OR name = %s)',
        (user_id, name)
    )

    # Fetch data
    data = []
    for result in cursor:
        data.append({
            'user_id':result['user_id'],
            'name':result['name'],
            'registration_date':result['registration_date'],
            'fans':result['fans'],
            'avg_stars':result['avg_stars'],
            'review_count':result['review_count']
        })
    cursor.close()

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/get_reviews', methods=['POST'])
def get_reviews():
    # Get data from forms
    review_id = request.form['review_id']
    business_id = request.form['business_id']
    user_id = request.form['user_id']

    # Execute query
    cursor = g.conn.execute(
        'SELECT * FROM Reviews WHERE \
            (review_id = %s OR business_id = %s OR user_id = %s)',
        (review_id, business_id, user_id)
    )

    # Fetch data
    data = []
    for result in cursor:
        data.append({
            'review_id':result['review_id'],
            'business_id':result['business_id'],
            'user_id':result['user_id'],
            'review_date':result['review_date'],
            'stars':result['stars'],
            'review_text':result['review_text'],
            'useful_count':result['useful_count'],
        })
    cursor.close()

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)


"""Complex Queries"""
# TODO:
@app.route('/get_busy_business', methods=['POST'])
def get_busy_business():
    # Get data from forms
    checkins = request.form['checkins']
    ratings = request.form['ratings']

    # Execute query
    cursor = g.conn.execute(
        'SELECT B1.name, B1.address, M.blob_data \
        FROM Business B1 INNER JOIN Media M ON B1.business_id = M.business_id \
        WHERE \
            B1.business_id IN ((SELECT B2.business_id \
                                FROM Business B2 \
                                WHERE B2.avg_stars > %s) \
                                INTERSECT \
                                (SELECT C.business_id \
                                FROM Checkins C \
                                GROUP BY C.business_id \
                                HAVING COUNT(C.business_id) > %s))',
        (ratings, checkins)
    )

    # Fetch data
    data = []
    for result in cursor:
        data.append({
            'name':result['name'],
            'address':result['address'],
            'blob_data':result['blob_data']
        })
    cursor.close()

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/get_friend_tips', methods=['POST'])
def get_friend_tips():
    # Get data from forms
    user_id = request.form['user_id']

    # Execute query
    cursor = g.conn.execute(
        'SELECT U.name AS user_name, B.name AS business_name, T.tip_text \
        FROM Yelp_User U, Business B, Tips T \
        WHERE U.user_id = T.user_id AND T.business_id = B.business_id \
        AND \
            U.user_id IN ((SELECT F.user_two_id AS friends_of_user_one \
                          FROM Yelp_User U, Friend_Of F \
                          WHERE U.user_id = F.user_one_id AND U.user_id = %s) \
                          UNION \
                          (SELECT F.user_two_id AS friends_of_user_one \
                          FROM Yelp_User U, Friend_Of F \
                          WHERE U.user_id = F.user_two_id AND U.user_id = %s))',
        (user_id, user_id)
    )

    # Fetch data
    data = []
    for result in cursor:
        data.append({
            'user_name':result['user_name'],
            'business_name':result['business_name'],
            'tip_text':result['tip_text']
        })
    cursor.close()

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/get_users_city', methods=['POST'])
def get_users_city():
    # Get data from forms
    city = request.form['city']

    # Execute query
    cursor = g.conn.execute(
        'SELECT U.user_id, U.name \
        FROM Yelp_User U \
        WHERE U.user_id IN \
            (SELECT R.user_id \
            FROM Reviews R \
            WHERE EXISTS \
                (SELECT * \
                FROM Business B \
                WHERE B.city = %s AND R.business_id = B.business_id))',
        (city)
    )

    # Fetch data
    data = []
    for result in cursor:
        data.append({
            'user_id':result['user_id'],
            'name':result['name']
        })
    cursor.close()

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/get_friend_reviewed', methods=['POST'])
def get_friend_reviewed():
    # Get data from forms
    user_id = request.form['user_id']

    # Execute query
    cursor = g.conn.execute(
        'SELECT business_id FROM reviews R \
        JOIN \
            (SELECT user_one_id AS u_id FROM Friend_of WHERE user_two_id = %s \
            UNION \
            SELECT user_two_id AS u_id FROM Friend_of WHERE user_one_id = %s) F \
        ON R.user_id = F.u_id \
        WHERE business_id NOT IN ( \
            SELECT business_id FROM reviews \
            WHERE user_id = %s \
        )',
        (user_id, user_id, user_id)
    )

    # Fetch data
    data = []
    if cursor:
        for result in cursor:
            data.append({
                'business_id':result['business_id']
            })
    cursor.close()

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)


# TODO:
@app.route('/get_visit_city', methods=['POST'])
def get_visit_city():
    # Get data from forms
    city = request.form['city']

    # Execute query
    cursor = g.conn.execute(
        'SELECT R.review_text, B.name FROM reviews R \
        JOIN business B ON B.business_id = R.business_id \
        WHERE B.city = %s AND R.useful_count > 0',
        (city)
    )

    # Fetch data
    data = []
    if cursor:
        for result in cursor:
            data.append({
                'review_text':result['review_text'],
                'name':result['name']
            })
    cursor.close()

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/get_users_enjoyed', methods=['POST'])
def get_users_enjoyed():
    # Get data from forms
    business_id = request.form['business_id']

    # Execute query
    cursor = g.conn.execute(
        'SELECT Y.name FROM yelp_user Y \
        JOIN reviews R ON R.user_id = Y.user_id \
        JOIN business B ON B.business_id = R.business_id \
        WHERE B.business_id = %s AND CAST(R.stars AS REAL) >= B.avg_stars',
        (business_id)
    )

    # Fetch data
    data = []
    if cursor:
        for result in cursor:
            data.append({
                'name':result['name']
            })
    cursor.close()

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/insert_reviews', methods=['POST'])
def insert_reviews():
    # Get data from forms
    business_id = request.form['business_id']
    user_id = request.form['user_id']
    review_date = request.form['review_date']
    stars = request.form['stars']
    review_text = request.form['review_text']
    useful_count = request.form['useful_count']

    # Set the sequence to the next value
    g.conn.execute("""SELECT setval('reviews_review_id_seq', max(review_id)) FROM Reviews;""")

    # Execute query
    # review_id will auto increment here
    g.conn.execute(
        'INSERT INTO Reviews \
            (review_id, business_id, user_id, review_date, stars, review_text, useful_count) \
        VALUES \
            (DEFAULT, %s, %s, %s, %s, %s ,%s)',
        (business_id, user_id, review_date, stars, review_text, useful_count)
    )

    return render_template("index.html")

# TODO:
@app.route('/insert_tips', methods=['POST'])
def insert_tips():
    # Get data from forms
    business_id = request.form['business_id']
    user_id = request.form['user_id']
    compliment_count = request.form['compliment_count']
    tip_date = request.form['tip_date']
    tip_text = request.form['tip_text']

    # Execute query
    g.conn.execute(
        'INSERT INTO Tips \
            (business_id, user_id, compliment_count, tip_date, tip_text) \
        VALUES \
            (%s, %s, %s, %s ,%s)',
        (business_id, user_id, compliment_count, tip_date, tip_text)
    )

    return render_template("index.html")

# TODO:
@app.route('/insert_friends', methods=['POST'])
def insert_friends():
    # Get data from forms
    user_one_id = request.form['user_one_id']
    user_two_id = request.form['user_two_id']

    # Set the sequence to the next value
    g.conn.execute("""SELECT setval('friend_of_friendship_id_seq', max(friendship_id)) FROM Friend_Of;""")

    # Execute query
    g.conn.execute(
        'INSERT INTO Friend_Of \
            (friendship_id, user_one_id, user_two_id) \
        VALUES \
            (DEFAULT, %s, %s)',
        (user_one_id, user_two_id)
    )

    return render_template("index.html")

# TODO:
@app.route('/insert_checkins', methods=['POST'])
def insert_checkins():
    # Get data from forms
    business_id = request.form['business_id']
    checkin_date = request.form['checkin_date']

    # Execute query
    g.conn.execute(
        'INSERT INTO Checkins \
            (business_id, checkin_date) \
        VALUES \
            (%s, %s)',
        (user_one_id, user_two_id)
    )

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/update_reviews_useful', methods=['POST'])
def update_reviews_useful():
    # Get data from forms
    review_id = request.form['review_id']

    # Execute query
    g.conn.execute(
        'UPDATE Reviews \
        SET useful_count = useful_count + 1 \
        WHERE review_id = %s',
        (review_id)
    )

    # Return updated value
    cursor = g.conn.execute(
        'SELECT review_id, useful_count \
        FROM Reviews \
        WHERE review_id = %s',
        (review_id)
    )

    # Fetch data
    data = []
    if cursor:
        for result in cursor:
            data.append({
                'review_id':result['review_id'],
                'useful_count':result['useful_count']
            })
    cursor.close()

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)


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
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()
