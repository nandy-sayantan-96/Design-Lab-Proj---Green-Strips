from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'green_strips'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute(""" SELECT * FROM responses """)
    res = cur.fetchall()
    print(res)
    cur.close()
    return str(res)



if __name__ == '__main__':
    app.run()