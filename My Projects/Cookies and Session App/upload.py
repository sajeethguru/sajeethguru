from flask import Flask,render_template,redirect,url_for,request,make_response,session

app = Flask(__name__)
app.secret_key = "Sajeeth"

@app.route('/')
def cookie():
    if 'user id' in session:
        id = session['user id']
        return 'Logged in as ' + id + '<br>' + '<b><a href ="/readcookie">click here to read cookie</a> ' + '<br>' + "<b><a href='/logout'>click here to log out</a></b>"
    return "<b><a href ='/login'>click here to login</a></b>"

@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user id',None)
    return redirect(url_for('cookie'))

@app.route('/setcookie',methods=["POST"])
def set_cookie():
    if request.method == 'POST':
        user = request.form['id']
        session['user id'] = user
        resp = make_response(render_template('success.html'))
        resp.set_cookie('user id',user)
        return resp

@app.route('/readcookie')
def read_cookie():
    id = request.cookies.get('user id')
    return "<h1>Welcome " + id + "</h1>" + '<br>' + '<b><a href="/logout">click here to logout</a></b>'

if __name__ == "__main__":
    app.run(debug = True)
