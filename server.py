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
#DATABASEURI = "postgresql://jn2717:amaurylovesalex@34.74.165.156/proj1part2"
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
db.tabulate_friends()

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

    name = '%%' + name + '%%'
    address = '%%' + address + '%%'
    city = '%%' + city + '%%'
    state = '%%' + state + '%%'

    # Execute query
    if business_id != '':
        cursor = g.conn.execute(
            'SELECT * FROM Business WHERE \
                business_id = %s AND \
                name ILIKE %s AND \
                address ILIKE %s AND \
                city ILIKE %s AND \
                state ILIKE %s',
            (business_id, name, address, city, state)
        )
    else:
        cursor = g.conn.execute(
            'SELECT * FROM Business WHERE \
                name ILIKE %s AND \
                address ILIKE %s AND \
                city ILIKE %s AND \
                state ILIKE %s \
                LIMIT 15',
            (name, address, city, state)
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

    #No data
    if data == []:
        data = [{'Message': 'Sorry, no business found.'}]
    
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

    name = '%%' + name + '%%'

    # Execute query
    if user_id != '':
        cursor = g.conn.execute(
            'SELECT * FROM Yelp_User WHERE \
                user_id = %s AND \
                name ILIKE %s',
            (user_id, name)
        )
    else:
        cursor = g.conn.execute(
            'SELECT * FROM Yelp_User WHERE \
                name ILIKE %s \
                LIMIT 15',
            (name)
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

    #No data
    if data == []:
        data = [{'Message': 'Sorry, no user found.'}]

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

    if review_id != '':
        if business_id != '':
            if user_id != '':
                cursor = g.conn.execute(
                    'SELECT * FROM Reviews WHERE \
                        review_id = %s AND \
                        business_id = %s AND \
                        user_id = %s',
                    (review_id, business_id, user_id)
                )
            else:
                cursor = g.conn.execute(
                    'SELECT * FROM Reviews WHERE \
                        review_id = %s AND \
                        business_id = %s',
                    (review_id, business_id)
               ) 

        else:
            if user_id != '':
                cursor = g.conn.execute(
                    'SELECT * FROM Reviews WHERE \
                        review_id = %s AND \
                        user_id = %s',
                    (review_id, user_id)
                )
            else:
                cursor = g.conn.execute(
                    'SELECT * FROM Reviews WHERE \
                        review_id = %s',
                    (review_id)
                )
    else:
        if business_id != '':
            if user_id != '':
                cursor = g.conn.execute(
                    'SELECT * FROM Reviews WHERE \
                        business_id = %s AND \
                        user_id = %s',
                    (business_id, user_id)
                )
            else:
                cursor = g.conn.execute(
                    'SELECT * FROM Reviews WHERE \
                        business_id = %s',
                    (business_id)
               ) 

        else:
            if user_id != '':
                cursor = g.conn.execute(
                    'SELECT * FROM Reviews WHERE \
                        user_id = %s',
                    (user_id)
                )
            else:
                cursor = g.conn.execute(
                    'SELECT * FROM Reviews LIMIT 15'
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

    #No data
    if data == []:
        data = [{'Message': 'Sorry, no review found.'}]
    
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

    if checkins != '' and ratings != '':
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

        # If no data
        if data == []:
            data = [{'Message': 'No busy businesses found!'}]

        cursor.close()
    else:
        data = [{'Error': 'Please enter checkins and ratings!'}]

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/get_friend_tips', methods=['POST'])
def get_friend_tips():
    # Get data from forms
    user_id = request.form['user_id']

    # Error handling
    if user_id != '':
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

        # If no data then return nothing found
        if data == []:
            data = [{'Message': 'No Tips found! User id not valid or please \
            add more friends!'}]

        cursor.close()
    else:
        data = [{'Error': 'Please enter a friend id!'}]


    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/get_users_city', methods=['POST'])
def get_users_city():
    # Get data from forms
    city = request.form['city']

    if city != '':
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

        if data == []:
            data = [{'Message': 'No users found!'}]
    else:
        data = [{'Error': 'Please enter a city!'}]

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/get_friend_reviewed', methods=['POST'])
def get_friend_reviewed():
    # Get data from forms
    user_id = request.form['user_id']

    if user_id != '':
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

        if data == []:
            data = [{'Message': 'No businesses found!'}]
    else:
        data = [{'Error': 'Please enter a user_id!'}]

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)


# TODO:
@app.route('/get_visit_city', methods=['POST'])
def get_visit_city():
    # Get data from forms
    city = request.form['city']

    if city != '':
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

        if data == []:
            data = [{'Message': 'No reviews found!'}]
    else:
        data = [{'Error': 'Please enter a city!'}]

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/get_users_enjoyed', methods=['POST'])
def get_users_enjoyed():
    # Get data from forms
    business_id = request.form['business_id']

    if business_id != '':

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

        if data == []:
            data = [{'Message': 'No users found!'}]
    else:
        data = [{'Error': 'Please enter a business_id!'}]

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

    if business_id != '' and user_id != '' and review_date != '' \
    and stars != '' and review_text != '' and useful_count != '':

        # Set the sequence to the next value
        g.conn.execute("""SELECT setval('reviews_review_id_seq', max(review_id)) FROM Reviews;""")

        # Execute query
        # review_id will auto increment here
        try:
            g.conn.execute(
                'INSERT INTO Reviews \
                    (review_id, business_id, user_id, review_date, stars, review_text, useful_count) \
                VALUES \
                    (DEFAULT, %s, %s, %s, %s, %s ,%s)',
                (business_id, user_id, review_date, stars, review_text, useful_count)
            )

            # Return updated value
            cursor = g.conn.execute(
                'SELECT * FROM Reviews ORDER BY review_id DESC LIMIT 1'
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
        except:
            data = [{'Error': 'Please make sure all inputs are VALID!'}]

    else:
        data = [{'Error': 'Please enter all inputs!'}]

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/insert_tips', methods=['POST'])
def insert_tips():
    # Get data from forms
    business_id = request.form['business_id']
    user_id = request.form['user_id']
    compliment_count = request.form['compliment_count']
    tip_date = request.form['tip_date']
    tip_text = request.form['tip_text']

    if business_id != '' and user_id != '' and compliment_count != '' \
    and tip_date != '' and tip_text != '':

        try:
            # Execute query
            g.conn.execute(
                'INSERT INTO Tips \
                    (business_id, user_id, compliment_count, tip_date, tip_text) \
                VALUES \
                    (%s, %s, %s, %s, %s)',
                (business_id, user_id, compliment_count, tip_date, tip_text)
            )

            data = [{'business_id': business_id, 'user_id': user_id,
                    'compliment_count':compliment_count, 'tip_date': tip_date,
                    'tip_text': tip_text}]
        except:
            data = [{'Error': 'Please make sure all inputs are VALID!'}]
    else:
        data = [{'Error': 'Please enter all inputs!'}]

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/insert_friends', methods=['POST'])
def insert_friends():
    # Get data from forms
    user_one_id = request.form['user_one_id']
    user_two_id = request.form['user_two_id']

    if user_one_id != '' and user_two_id != '':
        # Set the sequence to the next value
        g.conn.execute("""SELECT setval('friend_of_friendship_id_seq', max(friendship_id)) FROM Friend_Of;""")

        try:
            # Check if friend one is a friends with friends two
            # or if friend two is friends with friend one
            cursor_one = g.conn.execute('SELECT * FROM Friend_Of WHERE user_one_id = %s AND user_two_id = %s', (user_one_id, user_two_id))
            cursor_two = g.conn.execute('SELECT * FROM Friend_Of WHERE user_one_id = %s AND user_two_id = %s', (user_two_id, user_one_id))
            not_friends = True
            for result in cursor_one:
                if result:
                    not_friends = False
            for result in cursor_two:
                if result:
                    not_friends = False
            cursor_one.close()
            cursor_two.close()


            if not_friends:
                # Execute query
                g.conn.execute(
                    'INSERT INTO Friend_Of \
                        (friendship_id, user_one_id, user_two_id) \
                    VALUES \
                        (DEFAULT, %s, %s)',
                    (user_one_id, user_two_id)
                )

                # Return the new value
                cursor = g.conn.execute(
                    'SELECT * FROM Friend_Of ORDER BY friendship_id DESC LIMIT 1'
                )

                # Fetch data
                data = []
                for result in cursor:
                    data.append({
                        'friendship_id':result['friendship_id'],
                        'user_one_id':result['user_one_id'],
                        'user_two_id':result['user_two_id']
                    })
                cursor.close()
            else:
                data = [{'Message': 'User One is already friends with User Two!'}]
        except:
            data = [{'Error': 'Please make sure all inputs are VALID!'}]
    else:
        data = [{'Error': 'Please enter all inputs!'}]

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/insert_checkins', methods=['POST'])
def insert_checkins():
    # Get data from forms
    business_id = request.form['business_id']
    checkin_date = request.form['checkin_date']

    if business_id != '' and checkin_date != '':
        try:
            # Execute query
            g.conn.execute(
                'INSERT INTO Checkins \
                    (business_id, checkin_date) \
                VALUES \
                    (%s, %s)',
                (business_id, checkin_date)
            )
            data = [{'business_id': business_id, 'checkin_date': checkin_date}]
        except:
            data = [{'Error': 'Please make sure your inputs are VALID!'}]
    else:
        data = [{'Error': 'Please enter all inputs!'}]

    # Send to View
    context = dict(data=data)
    return render_template("index.html", **context)

# TODO:
@app.route('/update_reviews_useful', methods=['POST'])
def update_reviews_useful():
    # Get data from forms
    review_id = request.form['review_id']

    if review_id != '':
        try:
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

            if data == []:
                data = [{'Message': 'Review ID not found!'}]
        except:
            data = [{'Error': 'Please make sure all inputs are VALID!'}]
    else:
        data = [{'Error': 'Please enter all inputs!'}]

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
