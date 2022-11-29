from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re
from flask_mail import Mail,Message
 
app = Flask(__name__)
app.config['MAIL_SERVER']='mail.smartinternz.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME'] = '810019106068@smartinternz.com'
app.config['MAIL_PASSWORD'] = 'PNTIBMCk77'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL']=True
mail = Mail(app)
 
app.secret_key='a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=Cert.crt;UID=pcj17018;PWD=MPcY3wjqbL7MbLBm",'','')


@app.route('/')
def home():
    session['loggedin']=False
    return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg=''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username=? AND password=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if(account):
            session['loggedin']=True
            session['id']=account['USERNAME']
            userid = account['USERNAME']
            session['USERNAME']=account['USERNAME']
            msg='Welcome %s!'%userid
            email=account['EMAIL']
            session['EMAIL']=email
            msg1=Message("Confirmation",sender='810019106068@smartinternz.com',recipients=[email])
            msg1.body="you have logged in to TRENDZ! Enjoy Shopping."
            mail.send(msg1)
            return render_template('home.html',msg=msg)
        else:
            msg="Incorrect username/password"
    return render_template('login.html',msg=msg)



@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg='Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg='Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg='Name must contain only characters and numbers!'
        else:
            insert_sql ="INSERT INTO users VALUES(?,?,?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.execute(prep_stmt)
            msg='you have successfully registered!'
            msg1=Message("Confirmation",sender='810019106068@smartinternz.com',recipients=[email])
            msg1.body="Hurray! You have Successfully registered"
            mail.send(msg1)
    elif request.method == 'POST':
        msg = 'Please fill out the form'
    return render_template('register.html',msg=msg)

@app.route('/alogin',methods=['GET','POST'])
def alogin():
    global adminid
    msg=''

    if request.method == 'POST':
        aname = request.form['aname']
        apassword = request.form['apassword']
        sql = "SELECT * FROM ADMIN WHERE NAME=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,aname)
        ibm_db.bind_param(stmt,2,apassword)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if(account):
            session['aloggedin']=True
            session['aid']=account['NAME']
            adminid = account['NAME']
            session['NAME']=account['NAME']
            msg='Welcome %s!'%adminid
            return render_template('admin.html',msg=msg)
        else:
            msg="Incorrect username/password"
    return render_template('adminlogin.html',msg=msg)



@app.route('/areg',methods=['GET','POST'])
def aregister():
    msg=''
    if request.method == 'POST':
        username = request.form['aname']
        email = request.form['aemail']
        password = request.form['apassword']
        sql = "SELECT * FROM ADMIN WHERE NAME=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg='Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg='Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg='Name must contain only characters and numbers!'
        else:
            insert_sql ="INSERT INTO admin VALUES(?,?,?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.execute(prep_stmt)
            msg='you have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form'
    return render_template('adminreg.html',msg=msg)

@app.route('/home')
def homepage():
    if session['loggedin']==True:
        msg='Welcome %s!'%userid
        return render_template('home.html',msg=msg)
    else:
        msg='Please Login!'
        return render_template('login.html',msg=msg)

@app.route('/shop')
def shop():
    if session['loggedin']==True:
        return render_template('shop.html')
    else:
        msg="Please Login!"
        return render_template('login.html',msg=msg)

@app.route('/product/<p1>')
def product(p1):
    img = 'https://sajee.s3.ap.cloud-object-storage.appdomain.cloud/products/%s.jpg' %p1
    print(img)
    product=p1
    sql="SELECT * FROM PRODUCT WHERE NAME =?"
    stmt=ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,product)
    ibm_db.execute(stmt)
    pro_sql="SELECT PRICE,PRONAME FROM PRODUCT WHERE NAME =?"
    pro_stmt=ibm_db.prepare(conn,pro_sql)
    ibm_db.bind_param(pro_stmt,1,product)
    ibm_db.execute(pro_stmt)
    tuple=ibm_db.fetch_tuple(pro_stmt)
    print(tuple)
    price=tuple[0]
    name=tuple[1]
    return render_template('product.html',img=img,price=price,name=name,product=product)

@app.route('/admin')
def admin():
    if session['aloggedin']==True:
        msg='Welcome %s!'%adminid
        return render_template('admin.html',msg=msg)
    else:
        msg='Please Login!'
        return render_template('adminlogin.html',msg=msg)

@app.route('/logout')
def logout():
    session['loggedin']=False
    session.pop('id',None)
    session.pop('USERNAME',None)
    return render_template('login.html')

@app.route('/alogout')
def alogout():
    session['aloggedin']=False
    session.pop('aid',None)
    session.pop('NAME',None)
    return render_template('adminlogin.html')

@app.route('/cart')
def cart():
    if session['loggedin']==True:
        sql_c="SELECT COUNT(NAME) FROM CART1"
        stmt_c=ibm_db.prepare(conn,sql_c)
        ibm_db.execute(stmt_c)
        count1=ibm_db.fetch_tuple(stmt_c)
        print(count1[0])
        count=count1[0]
        sql_name="SELECT NAME FROM CART1"
        stmt_name=ibm_db.prepare(conn,sql_name)
        ibm_db.execute(stmt_name)
        name=ibm_db.fetch_assoc(stmt_name)
        print(name)
        
        sql_price="SELECT PRICE FROM CART1"
        stmt_price=ibm_db.prepare(conn,sql_price)
        ibm_db.execute(stmt_price)
        price=ibm_db.fetch_both(stmt_price)
        print(price)
        
        sql_pro="SELECT PRONAME FROM CART1"
        stmt_pro=ibm_db.prepare(conn,sql_pro)
        ibm_db.execute(stmt_pro)
        proname=ibm_db.fetch_tuple(stmt_pro)
        print(proname)

        sql_img="SELECT LINK FROM CART1"
        stmt_img=ibm_db.prepare(conn,sql_img)
        ibm_db.execute(stmt_img)
        img=ibm_db.fetch_tuple(stmt_img)

        return render_template('cart.html',count=count,img=img,proname=proname,price=price,product=name)
    else:
        msg='Please Login!'
        return render_template('login.html',msg=msg)

@app.route('/addcart/<product>')
def add_cart(product):
    p=product
    sql="SELECT NAME,PRICE,LINK,PRONAME FROM PRODUCT WHERE NAME=?"
    stmt=ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,p)
    ibm_db.execute(stmt)
    cart=ibm_db.fetch_tuple(stmt)
    name=cart[0]
    price=cart[1]
    link=cart[2]
    proname=cart[3]
    cart_sql="INSERT INTO CART1 values(?,?,?,?)"
    cart_stmt=ibm_db.prepare(conn,cart_sql)
    ibm_db.bind_param(cart_stmt,1,name)
    ibm_db.bind_param(cart_stmt,2,price)
    ibm_db.bind_param(cart_stmt,3,link)
    ibm_db.bind_param(cart_stmt,4,proname)
    ibm_db.execute(cart_stmt)
    msg='successfully added to cart!'
    return render_template('home.html',msg=msg)

@app.route('/buy/<product>')
def buy(product):
    p=product
    sql="SELECT NAME,PRICE,PRONAME FROM PRODUCT WHERE NAME=?"
    stmt=ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,p)
    ibm_db.execute(stmt)
    cart=ibm_db.fetch_tuple(stmt)
    name=cart[0]
    price=cart[1]
    id=session['id']
    pro=cart[2]
    email=session['EMAIL']
    buy_sql="INSERT INTO BUY1 values(?,?,?)"
    buy_stmt=ibm_db.prepare(conn,buy_sql)
    ibm_db.bind_param(buy_stmt,1,id)
    ibm_db.bind_param(buy_stmt,2,name)
    ibm_db.bind_param(buy_stmt,3,price)
    ibm_db.execute(buy_stmt)
    msg='Successfully Purchased!'
    msg1=Message("Purchase Confirmation",sender='810019106068@smartinternz.com',recipients=[email])
    msg1.body="You Have Purchased the product:%s Successfully!"%pro
    mail.send(msg1)

    return render_template('home.html',msg=msg)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')