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
    loggedIn, name = getLoginDetails()
    return render_template('home.html', user_data = name)

#Fetch user details if logged in
def getLoginDetails():
    if 'email' not in session:
        loggedIn = False
        name = 'GUEST'
    else:
        loggedIn = True
        name = session['name']
    return (loggedIn, name)


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
            session['user_id'] = user['id']
            #return "LOGIN SUCCESS"
            return redirect(url_for('products'))
        else:
            return "Passwords not match"

    else :
        return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout_user():
    session.clear()
    return redirect(url_for('index'))

@app.route('/products')
def products():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM products ")
    prods = cur.fetchall()
    cur.close()
    return render_template('products.html', prods = prods)

@app.route('/advertise')
def advertise():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM products ")
    prods = cur.fetchall()
    cur.close()
    return render_template('advertisement.html', prods = prods)

@app.route('/addToCart/<int:prod_id>', methods=['POST'])
def addToCart(prod_id, purchase_type = 0):
    loggedIn = getLoginDetails()[0]
    if loggedIn == False:
        return redirect(url_for('login_user'))
    user_id = session['user_id']
    qty = request.form['qty']
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cart (user_id, product_id, qty, purchase_type) VALUES (%s, %s, %s, %s)",
                (user_id, prod_id, qty, purchase_type,))

        mysql.connection.commit()
        msg = "Added to Cart Successfully"
        print(msg)
    except:
        mysql.connection.rollback()
        msg = "Error occured"
        print(msg)
        return msg
    cur.close()
    return redirect(url_for('products'))

@app.route('/addToCartAdvertise/<int:prod_id>', methods=['POST'])
def addToCartAdvertise(prod_id):
    addToCart(prod_id, 1)
    return redirect(url_for('advertise'))

@app.route('/cart')
def cart():
    user_id = session['user_id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM cart WHERE user_id = %s", (user_id,))
    cart_prods = cur.fetchall()
    cur.close()
    return render_template('cart.html', cart_prods = cart_prods)

if __name__ == '__main__':
    app.secret_key = "dsadasdsadqw2346436%nw9e"
    app.run(debug=True)