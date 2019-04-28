import json

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)

##Database connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'green_strips'
mysql = MySQL(app)


@app.route('/')
def index():
    loggedIn, name = getLoginDetails()
    return render_template('index.html', user_data=name)


# Fetch user details if logged in
@app.route('/loggedin', methods=['GET', 'POST'])
def check_login():
    loggedIn, name = getLoginDetails()
    return jsonify({'status': loggedIn, 'name': name})


def getLoginDetails():
    if 'email' not in session:
        loggedIn = False
        name = 'GUEST'
    else:
        loggedIn = True
        name = session['name']
    return loggedIn, name


@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    return render_template('register.html')


@app.route('/buyForm', methods=['GET', 'POST'])
def buy_form():
    return render_template('buyform.html')


@app.route('/advertiseForm', methods=['GET', 'POST'])
def advertise_form():
    return render_template('advertiseform.html')


@app.route('/register', methods=['POST'])
def register_advertiser():
    if request.method == 'POST':
        # Parse form data
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address = request.form['address']
        organization = request.form['organization']
        phone = request.form['phone']
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO advertisers (f_name, l_name, organization, address, email, phone, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (firstName, lastName, organization, address, email, phone, password,))
            # (hashlib.md5(password.encode()).hexdigest()

            mysql.connection.commit()
            msg = "Registered Successfully"
            print(msg)
        except:
            mysql.connection.rollback()
            msg = "Error occured"
            print(msg)
            return jsonify({'status': False, 'message': msg})
        cur.close()
        return jsonify({'status': True, 'message': msg})


@app.route('/login', methods=['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(" SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user is None:
            flash("Email not registered")
            return redirect(url_for('login_user'))

        if password == user['password']:
            session['email'] = user['email']
            session['name'] = user['f_name']
            session['user_id'] = user['id']
            flash('You were successfully logged in')
            return redirect(url_for('index'))
        else:
            flash("Incorrect Password")
            return redirect(url_for('login_user'))

    else:
        return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout_user():
    session.clear()
    msg = "User Logged Out!"
    return jsonify({'status': True, 'message': msg})


@app.route('/products')
def products():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM products ")
    prods = cur.fetchall()
    cur.close()
    return render_template('buypage.html', prods=prods)


@app.route('/advertise')
def advertise():
    loggedIn = getLoginDetails()[0]

    if not loggedIn:
        return redirect(url_for('login_user'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM products ")
    prods = cur.fetchall()
    cur.close()
    return render_template('advertisepage.html', prods=prods)


# @app.route('/addToCart/<int:prod_id>', methods=['POST'])
def addToCart(prod_id, purchase_type=0):
    loggedIn = getLoginDetails()[0]
    if not loggedIn:
        return redirect(url_for('login_user'))
    user_id = session['user_id']
    qty = request.form['qty']
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cart (user_id, product_id, qty, purchase_type) VALUES (%s, %s, %s, %s)",
                    (user_id, prod_id, qty, purchase_type,))

        mysql.connection.commit()
        msg = "Added to Cart Successfully"
        flash(msg)

    except:
        mysql.connection.rollback()
        msg = "Error occured"
        flash(msg)
        return redirect(url_for('advertise'))
        # return {'status': False, 'message': msg}
    cur.close()
    return redirect(url_for('advertise'))


@app.route('/addToCartAdvertise/<int:prod_id>', methods=['POST'])
def addToCartAdvertise(prod_id):
    addToCart(prod_id, 1)
    return redirect(url_for('advertise'))
    # return response


'''
@app.route('/checkCart', methods=['POST'])
def check_cart():
    user_id = session['user_id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT 1 FROM cart WHERE user_id = %s", (user_id,))
    cart_prods = cur.fetchall()
    cur.close()
    if len(cart_prods) > 0:
        msg = "Products exist in cart"
        return jsonify({'status': True, 'message': msg})
    else:
        msg = "No products in your cart"
        return jsonify({'status': False, 'message': msg})
'''


@app.route('/cart')
def cart():
    loggedIn = getLoginDetails()[0]
    if not loggedIn:
        return redirect(url_for('login_user'))
    user_id = session['user_id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM cart WHERE user_id = %s", (user_id,))
    cart_prods = cur.fetchall()
    cur.close()
    return render_template('user.html', cart_prods=cart_prods)


@app.route('/cart_item/remove/<int:cart_item_id>', methods = ['POST'])
def removerCartItem(cart_item_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM cart WHERE cart_item_id = %s", (cart_item_id,))
        mysql.connection.commit()
        msg = "Removed from the Cart Successfully"
        print(msg)
    except:
        mysql.connection.rollback()
        msg = "Error occured"
        print(msg)
        return msg
    cur.close()
    return redirect(url_for('cart'))


@app.route('/order')
def order():
    loggedIn = getLoginDetails()[0]
    if not loggedIn:
        return redirect(url_for('login_user'))
    user_id = session['user_id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM order_details WHERE u_id = %s", (user_id,))
    order_prods = cur.fetchall()
    cur.close()
    return render_template('order.html', order_prods=order_prods)


@app.route('/checkout', methods=['POST'])
def checkout():
    cur = mysql.connection.cursor()
    cur.execute(" SELECT * FROM order_details ")
    orders = cur.fetchall()
    if len(orders) == 0:
        order_id = 1
    else:
        cur.execute(" SELECT o_id FROM order_details ORDER BY o_id DESC LIMIT 1")
        order_id = cur.fetchone()[0] + 1
    user_id = session['user_id']

    cur.execute(" SELECT user_id, product_id, SUM(qty), purchase_type FROM cart WHERE user_id = %s GROUP BY product_id, purchase_type ", (user_id,))
    cart_details = cur.fetchall()
    print(cart_details)
    for items in cart_details :
        print(items[1], "   ", items[2], items[3])
        try:
            cur.execute(" INSERT INTO order_details (o_id, p_id, u_id, qty, purchase_type) VALUES (%s, %s, %s, %s, %s)",
                        (order_id, items[1], user_id, items[2], items[3],))
            mysql.connection.commit()
            cur.execute(" DELETE FROM cart where user_id = %s", (user_id,))
            mysql.connection.commit()
        except:
            mysql.connection.rollback()
            msg = "Error occured"
            print(msg)
            return msg
    cur.close()

    return redirect(url_for('order'))


@app.route('/admin-login', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        name = request.form['name']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(" SELECT * FROM admin WHERE admin_name = %s", (name,))
        admin = cur.fetchone()
        cur.close()

        if admin == None:
            return " Wrong Admin!!! Intruder!!! Back Off Now!!!!!!!!!!!!!! "

        if password == admin['password'] :
            session['admin-login'] = True
            return redirect(url_for('admin_panel'))

        else:
            return "Passwords not match"

    else :
        return render_template('admin-login.html')


@app.route('/site/maintenance/admin-panel')
def admin_panel():
    try:
        if session['admin-login'] == True :
            cur = mysql.connection.cursor()
            cur.execute(" SELECT * FROM order_details ORDER BY o_id DESC ")
            order_details = cur.fetchall()
            cur.close()
            order_details_dict = {}

            for items in order_details:
                order_id = items[0]
                if order_id in order_details_dict.keys():
                    order_details_dict[order_id]['details'] += [[items[1], items[3], items[4]]]
                else:
                    order_details_dict[order_id] = {'user_id' : items[2]}
                    order_details_dict[order_id]['details'] = [[items[1], items[3], items[4]]]
                    order_details_dict[order_id]['status'] = items[5]
            print(order_details_dict)
            return render_template('admin-panel.html', order_details = order_details_dict, keys = order_details_dict.keys())
        else:
            return redirect(url_for('admin_panel'))
    except:
        return " Wrong Admin!!! Intruder!!! Back Off Now!!!!!!!!!!!!!! "


@app.route('/site/maintenance/delivery/status/update/<int:order_id>', methods = ['POST'])
def delivery_status_update(order_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(" UPDATE order_details SET deliveryandpayment = 'DONE' WHERE o_id = %s", (order_id,) )
        mysql.connection.commit()
        msg = "Successfully Completed"
        print(msg)
    except:
        mysql.connection.rollback()
        msg = "Error occured"
        print(msg)
        return msg
    cur.close()
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.secret_key = "dsadasdsadqw2346436%nw9e"
    app.run(debug=True)
