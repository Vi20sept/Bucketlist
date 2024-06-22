from flask import Flask, render_template, json, request, session, redirect
import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# SQL configurations is done finally to push in jenkins withe the help of vivek.
# Feature/Vivek-debug for debugging
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "SERVER={python-web-app1-server.database.windows.net};"
    "DATABASE={BucketList};"
    "UID=python-web-app1-server-admin;"
    "PWD=S65TWW48QC147WR4$;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=60;"
)

app.secret_key = 'Why would i tell'


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/signup')
def showSignUp():
    return render_template('signup.html')


@app.route('/signin')
def showSignin():
    return render_template('signin.html')


@app.route('/userHome')
def showuserhome():
    return render_template('userhome.html')


@app.route('/api/validateLogin', methods=['POST'])
def validateLogin():
    try:
        cursor = conn.cursor()
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # Simple SQL query to fetch user data
        query = "SELECT * FROM tbl WHERE user_username = ?"
        cursor.execute(query, (_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            session['user'] = data[0][0]
            return redirect('/userHome')
        else:
            return render_template('error.html', error='Wrong Email address or password')

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/api/signup', methods=['POST'])
def signUp():
    try:
        # Handle POST request
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # Validate the received values
        if _name and _email and _password:
            # Hash the password
            _hashed_password = (_password)

            # Simple SQL query to insert user data
            query = "INSERT INTO tbl (user_name,user_username, user_password) VALUES (?, ?, ?)"
            cursor = conn.cursor()
            cursor.execute(query, (_name, _email, _hashed_password))
            conn.commit()

            return json.dumps({'message': 'User created successfully!'})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0")
