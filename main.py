#required libraries/files/extensions imported
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import hashlib
from flask_mysqldb import MySQL, MySQLdb

#Some Global Data used by several functions
products_dict = {1: 'Book Store Bag', 2:'Medical Store Bag', 3:'Pamphlets'}
purchase_dict = {0: 'ADVERTISE AND BUY', 1:'ADVERTISE ' , 2:'BUY'}

#Flask object
app = Flask(__name__)
app.secret_key = 'nfhgtErY#$09&*!nnYYZZ8955'

##Database connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'green_strips'
mysql = MySQL(app)

#Home Page / Index Page of the website
@app.route('/')
def index():
    loggedIn, name = getLoginDetails()
    return render_template('index.html', user_data=name)


#Fetch user details if logged in
@app.route('/loggedin', methods=['GET', 'POST'])
def check_login():
    loggedIn, name = getLoginDetails()
    return jsonify({'status': loggedIn, 'name': name})

#Returns the name of the user if logged in
def getLoginDetails():
    if 'email' not in session:
        loggedIn = False
        name = 'GUEST'
    else:
        loggedIn = True
        name = session['name']
    return loggedIn, name

#Returns the User Registration/ Sign-Up
@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    return render_template('advertiseform.html')

#Returns the page containing all information about the logged in user
@app.route('/userDetails', methods=['GET', 'POST'])
def user_details():
    loggedIn, name = getLoginDetails()
    if not loggedIn:
        return redirect(url_for('login_user'))
    user_data = get_user_details()
    return render_template('user.html', user_data=user_data)

#Returns All detials of the logged in user
def get_user_details():
    loggedIn, name = getLoginDetails()
    if not loggedIn:
        return redirect(url_for('login_user'))
    else:
        user_id = session['user_id']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(" SELECT * FROM users WHERE id = %s", (user_id,))
        user_data = cur.fetchone()
        cur.close()
        return user_data

#Registers a new user; adds the user in the 'users' table
@app.route('/register', methods=['POST'])
def register_advertiser():
    if request.method == 'POST':
        # Parse form data
        password = request.form['password']
        password = hashlib.md5(password.encode()).hexdigest()
        email = request.form['email']
        firstName = request.form['f_name']
        lastName = request.form['l_name']
        address = request.form['address']
        organization = request.form['org_name']
        phone = request.form['phone']
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(
                "INSERT INTO users (f_name, l_name, organization, address, email, phone, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (firstName, lastName, organization, address, email, phone, password,))
            mysql.connection.commit()

            # On sucessful registration, log the user in
            cur.execute(" SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            session['email'] = user['email']
            session['name'] = user['f_name']
            session['user_id'] = user['id']
            flash('You were successfully registered')

        except Exception as exc:
            mysql.connection.rollback()
            msg = "Error occured"
            flash(str(exc))
            flash("One or Many Details Already Exists in the System. Contact Admin to retrive the account or Create a new one if required")
            return redirect(url_for('user_signup'))

        cur.close()
        return redirect(url_for('advertise'))

#Checks the entered details and allows legitimate users to log in
@app.route('/login', methods=['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        password = request.form['password']
        password = hashlib.md5(password.encode()).hexdigest()
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

#Allows the signed in User to Sign Out
@app.route('/logout', methods=['POST'])
def logout_user():
    session.clear()
    msg = "User Logged Out!"
    return jsonify({'status': True, 'message': msg})

'''
#Lists all available products
@app.route('/products')
def products():
    loggedIn, name = getLoginDetails()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM products ")
    prods = cur.fetchall()
    cur.close()
    return render_template('buy.html', prods=prods, user_data=name)
'''

#Directs to the products page; all purchase to be done from this page; user must to logged in to see this page
@app.route('/advertise')
def advertise():
    loggedIn, name = getLoginDetails()
    if not loggedIn:
        return redirect(url_for('login_user'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM products ")
    prods = cur.fetchall()
    cur.close()
    return render_template('advertise.html', prods=prods, user_data=name)


#Adds user selected items in the cart table of the database
def addToCart(prod_id):
    loggedIn = getLoginDetails()[0]
    if not loggedIn:
        return redirect(url_for('login_user'))
    user_id = session['user_id']
    qty = request.form['qty']
    purchase_type = request.form['side-book']
    if purchase_type == 'ssa':
        purchase_type = 0
    elif purchase_type == 'bsa':
        purchase_type = 1
    elif purchase_type == 'b':
        purchase_type = 2
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

#Allows users to add items to their carts
@app.route('/addToCartAdvertise/<int:prod_id>', methods=['POST'])
def addToCartAdvertise(prod_id):
    addToCart(prod_id)
    return redirect(url_for('advertise'))

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

#Displays the cart of the logged in user
@app.route('/cart')
def cart():
    loggedIn, name = getLoginDetails()
    if not loggedIn:
        return redirect(url_for('login_user'))
    user_id = session['user_id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(
        " SELECT * FROM cart JOIN products ON cart.product_id=products.p_id WHERE user_id = %s;",
        (user_id,))
    cart_prods = cur.fetchall()
    cur.close()
    for product in cart_prods:
        if product['purchase_type'] == 0:
            product['purchase_type'] = "Advertise and Buy"
            price = product['price_ad'] + product['price_buy']
        elif product['purchase_type'] == 1:
            product['purchase_type'] = "Advertise"
            price = product['price_ad']
        else:
            product['purchase_type'] = "Buy"
            price = product['price_buy']
        product['total_price'] = price * product['qty']
    return render_template('cart.html', cart_prods=cart_prods, user_data=name)

#Removes selected items from the cart of the user
@app.route('/cart_item/remove/<int:cart_item_id>', methods=['POST'])
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

#Places items in the cart to the order page
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
    cur.execute(
        " SELECT user_id, product_id, SUM(qty), purchase_type FROM cart WHERE user_id = %s GROUP BY product_id, purchase_type ",
        (user_id,))
    cart_details = cur.fetchall()

    for items in cart_details:
        print('##########')
        print(items[1])
        print('##########')
        cur.execute(" SELECT * FROM products WHERE p_id = %s;", (items[1],))
        product = cur.fetchone()
        print(product)
        if items[3] == 0:
            price = product[-1] + product[-2]
        elif items[3] == 1:
            price = product[-2]
        else:
            price = product[-1]
        total_price = price * items[2]
        try:
            cur.execute(" INSERT INTO order_details (o_id, p_id, u_id, qty, purchase_type, total_amount) VALUES (%s, %s, %s, %s, %s, %s)",
                        (order_id, items[1], user_id, items[2], items[3], total_price))
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

#Shows the order history of the user
'''
@app.route('/order')
def order():
    loggedIn, name = getLoginDetails()
    if not loggedIn:
        return redirect(url_for('login_user'))
    user_id = session['user_id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM order_details WHERE u_id = %s", (user_id,))
    order_prods = cur.fetchall()
    cur.close()
    return render_template('order.html', order_prods=order_prods, user_data=name,
                            products = products_dict, purchase = purchase_dict)
'''

@app.route('/order')
def order():
    loggedIn, name = getLoginDetails()
    if not loggedIn:
        return redirect(url_for('login_user'))
    user_id = session['user_id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(
        " SELECT * FROM order_details JOIN products ON order_details.p_id=products.p_id WHERE u_id = %s;",
        (user_id,))
    order_prods = cur.fetchall()
    cur.close()
    for product in order_prods:
        if product['purchase_type'] == 0:
            product['purchase_type'] = "Advertise and Buy"
            price = product['price_ad'] + product['price_buy']
        elif product['purchase_type'] == 1:
            product['purchase_type'] = "Advertise"
            price = product['price_ad']
        else:
            product['purchase_type'] = "Buy"
            price = product['price_buy']
        product['total_price'] = price * product['qty']
    return render_template('order.html', order_prods=order_prods, user_data=name)

#Admin-Login Page
@app.route('/admin-login', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        name = request.form['username']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(" SELECT * FROM admin WHERE admin_name = %s", (name,))
        admin_details = cur.fetchone()
        cur.close()

        if admin_details == None:
            return " Wrong Admin!!! Intruder!!! Back Off Now!!!!!!!!!!!!!! "

        elif password == admin_details['password']:
            session['admin-login'] = True
            return redirect(url_for('admin_panel'))

        else:
            return "Passwords not match"

    else:
        return render_template('admin-login.html')

#Opens up the admin panel
@app.route('/site/maintenance/admin-panel')
def admin_panel():
    try:
        if session['admin-login'] == True:
            cur = mysql.connection.cursor()
            cur.execute(" SELECT * FROM order_details ORDER BY o_id DESC ")
            order_details = cur.fetchall()
            cur.close()
            order_details_dict = {}

            for items in order_details:
                order_id = items[0]
                cur = mysql.connection.cursor()
                cur.execute(" SELECT f_name, l_name, address, email, phone FROM users WHERE id = %s", (items[2],))
                user_data = cur.fetchone()
                cur.close()

                if order_id in order_details_dict.keys():
                    order_details_dict[order_id]['details'] += [[products_dict[items[1]], items[3], purchase_dict[items[5]], items[4] ]]
                else:
                    order_details_dict[order_id] = {'user_details': user_data}
                    order_details_dict[order_id]['details'] = [[products_dict[items[1]], items[3], purchase_dict[items[5]], items[4] ]]
                    order_details_dict[order_id]['status'] = items[6]

            print(order_details_dict)
            return render_template('admin-panel.html', order_details=order_details_dict, keys=order_details_dict.keys())
        else:
            return redirect(url_for('admin_panel'))
    except:
        return render_template('admin-login.html')

#Changes the status of a particular order to delivered
@app.route('/site/maintenance/delivery/status/update/<int:order_id>', methods=['POST'])
def delivery_status_update(order_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(" UPDATE order_details SET deliveryandpayment = 'DONE' WHERE o_id = %s", (order_id,))
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

#log outs the admin
@app.route('/admin_logout', methods=['POST'])
def admin_logout():
    session.clear()
    msg = "User Logged Out!"
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
