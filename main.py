from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)

##Database connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'green_strips'
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        #Parse form data
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address = request.form['address']
        organization = request.form['organization']
        phone = request.form['phone']
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (f_name, l_name, organization, address, email, phone, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (firstName, lastName, organization, address, email, phone, password,))
            #(hashlib.md5(password.encode()).hexdigest()

            mysql.connection.commit()
            msg = "Registered Successfully"
            print(msg)
        except:
            mysql.connection.rollback()
            msg = "Error occured"
            print(msg)
            return msg
        cur.close()
        return redirect(url_for('index'))

@app.route('/login', methods=['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(" SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user == None:
            return "Email not registered"

        if password == user['password'] :
            session['email'] = user['email']
            session['name'] = user['f_name']
            #return "LOGIN SUCCESS"
            return redirect(url_for('index'))
        else:
            return "Passwords not match"

    else :
        return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout_user():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = "dsadasdsadqw2346436%nw9e"
    app.run()