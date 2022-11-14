from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

app = Flask(__name__)

hostname = '19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud'
uid = 'sfr69790'
pw = 'VFRS0bFKFeIhMbcq'
driver = "{IBM DB2 ODBC DRIVER}"
db_name = 'Bludb'
port = '30699'
protocol = 'TCPIP'
cert = "C:/Users/Prithiarun/Desktop/IBM/TEST/certi.crt"
dsn = (
    "DATABASE ={0};"
    "HOSTNAME ={1};"
    "PORT ={2};"
    "UID ={3};"
    "SECURITY=SSL;"
    "PROTOCOL={4};"
    "pw ={6};"
).format(db_name, hostname, port, uid, protocol, cert, pw)
connection = ibm_db.connect(dsn, "", "")
print()
# query = "SELECT username FROM USER1 WHERE username=?"
# statement = ibm_db.prepare(connection, query)
# ibm_db.bind_param(statement, 1, username)
# ibm_db.execute(statement)
# username = ibm_db.fetch_assoc(statement)
# print(username)
app.secret_key = 'a'


@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = " "
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        query = "SELECT * FROM USER1 WHERE username=?;"
        statement = ibm_db.prepare(connection, query)
        ibm_db.bind_param(statement, 1, username)
        ibm_db.execute(statement)
        account = ibm_db.fetch_assoc(statement)
        if (account):

            message = "Account already exists!"
            return render_template('register.html', message=message)
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     message = "Invalid email addres"
        # elif not re.match(r'[A-Za-z0-9+', username):
        #     message = "Name must contain only characters and numbers"
        else:
            query = "INSERT INTO USER1 values(?,?,?,?)"
            statement = ibm_db.prepare(connection, query)
            ibm_db.bind_param(statement, 1, username)
            ibm_db.bind_param(statement, 2, email)
            ibm_db.bind_param(statement, 3, phone)
            ibm_db.bind_param(statement, 4, password)
            ibm_db.execute(statement)
            message = 'You have successfully Logged In!!'
            return render_template('login.html', message=message)
    else:
        message = 'PLEASE FILL OUT OF THE FORM'
        return render_template('register.html', message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global userid
    message = ' '
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        query = "select * from user1 where username=? and password=?"
        statement = ibm_db.prepare(connection, query)
        ibm_db.bind_param(statement, 1, username)
        ibm_db.bind_param(statement, 2, password)
        ibm_db.execute(statement)
        account = ibm_db.fetch_assoc(statement)
        print(account)
        if account:
            session['Loggedin'] = True
            session['id'] = account['USERNAME']
            session['username'] = account['USERNAME']
            message = 'Logged in Successfully'
            return render_template('welcome.html', message=message, username=str.upper(username))
        else:
            message = 'Incorrect Username or Password'
            return render_template('login.html', message=message)
    else:
        message = 'PLEASE FILL OUT OF THE FORM'
        return render_template('login.html', message=message)


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        username = request.form['username']
        print(username)
        return render_template('welcome.html', username=username)
    else:
        return render_template('welcome.html', username=username)


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0')
