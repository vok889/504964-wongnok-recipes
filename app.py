# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import random

UPLOAD_FOLDER = "static/img/recipe/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.debug = True

app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'wongrok'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


mysql = MySQL(app)
print(mysql)

@app.route("/")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE email = % s \
            AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect email / password !'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    if 'loggedin' in session:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        return render_template("index.html")
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO accounts VALUES \
            (NULL, % s, % s, % s)',
                        (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

@app.route("/search", methods=['GET', 'POST'])
def search():
    msg = 'ผลลัพธ์การค้นหา "ต้มยำ"'
    rv = ''
    lenrv = 0
    if request.method == 'POST' and 'word_search' in request.form :
        word_search = request.form['word_search']
        word_search = "%"+word_search+"%"
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM recipe WHERE recipe_name like %s or recipe_ingredient like %s' , (word_search, word_search))
        rv = cursor.fetchall()
        lenrv = len(rv)
        msg = 'ผลลัพธ์การค้นหา "'+request.form['word_search']+'"'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template("search.html",o_recipe = rv, msg=msg, lenrv=lenrv)

@app.route("/myrecipe")
def myrecipe():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM recipe WHERE id = % s', (session['id'], ))
    rv = cursor.fetchall()
    print(len(rv))
    return render_template("myrecipe.html",o_recipe = rv)

@app.route("/addrecipe", methods=['GET', 'POST'])
def addrecipe():
    msg = ''
    print(request.form)
    if request.method == 'POST' and 'recipe_name' in request.form and 'recipe_category' in request.form and request.files['recipe_picture'].filename !="" and 'recipe_serving' in request.form and 'recipe_time' in request.form and 'recipe_level' in request.form and 'recipe_ingredient' in request.form and 'recipe_step' in request.form  :
        id=session['id']
        recipe_name = request.form['recipe_name']
        recipe_category = request.form['recipe_category']
        recipe_picture = request.files['recipe_picture'].filename
        recipe_serving = request.form['recipe_serving']
        recipe_time = request.form['recipe_time']
        recipe_level = request.form['recipe_level']
        recipe_ingredient = request.form['recipe_ingredient']
        recipe_step = request.form['recipe_step'] 
        
        frecipe_picture = request.files['recipe_picture']
        frecipe_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], frecipe_picture.filename))   
        print(str(id)+"="+str(recipe_name)+"="+str(recipe_category)+"="+str(recipe_picture)+"="+str(recipe_serving)+"="+str(recipe_time)+"="+str(recipe_level))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute(
        #     'SELECT * FROM recipe WHERE email = % s', (email, ))
        # account = cursor.fetchone()
        # if account:
        #     msg = 'Account already exists !'
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     msg = 'Invalid email address !'
        # elif not re.match(r'[A-Za-z0-9]+', username):
        #     msg = 'name must contain only characters and numbers !'
        # else:
        #     cursor.execute('INSERT INTO accounts VALUES \
        #     (NULL, % s, % s, % s)',
        #                 (username, password, email, ))
        #     mysql.connection.commit()
        #     msg = 'You have successfully registered !'
        cursor.execute('INSERT INTO recipe VALUES \
            (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s)',
            (id, recipe_name, recipe_category, recipe_picture, recipe_serving, recipe_time, recipe_level,recipe_ingredient,recipe_step,))
        mysql.connection.commit()
        msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template("addrecipe.html", msg=msg)


@app.route("/display")
def display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = % s',
                    (session['id'], ))
        account = cursor.fetchone()
        return render_template("display.html", account=account)
    return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and'address' in request.form and 'city' in request.form and 'country'in request.form and 'postalcode' in request.form and 'organisation' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            organisation = request.form['organisation']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            postalcode = request.form['postalcode']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM accounts WHERE username = % s',
                    (username, ))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE accounts SET username =% s,\
                password =% s, email =% s, organisation =% s, \
                address =% s, city =% s, state =% s, \
                country =% s, postalcode =% s WHERE id =% s', (
                    username, password, email, organisation, 
                address, city, state, country, postalcode, 
                (session['id'], ), ))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg=msg)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
