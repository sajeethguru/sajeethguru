from flask import Flask, render_template,request
app = Flask(__name__)

@app.route('/')
def login():
   return render_template('login.html')

@app.route('/login',methods =["POST"])
def hello_name():
   if request.method == "POST":
      x=request.form['name']
      y=request.form['email']
      z=request.form['ph']
      return render_template('login.html',name=x,email=y,ph=z)

if __name__ == '__main__':
   app.run(debug = True)