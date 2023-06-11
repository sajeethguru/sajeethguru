from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re
from datetime import datetime

app = Flask(__name__)

app.secret_key='a'

conn = ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port number;SECURITY=SSL;SSLServerCertificate=Cert.crt;UID=user id;PWD=password",'','')

@app.route('/')
def log():
    session['loggedin']=False
    return render_template('login.html')

@app.route('/flogin',methods=['GET','POST'])
def flogin():
    global userid
    msg1=''
    if request.method == 'POST':
        fmail = request.form['fmail']
        fpass = request.form['fpass']
        flsql = "SELECT * FROM FARMERS WHERE FMAIL = ? AND FPASSWORD = ?"
        flstmt = ibm_db.prepare(conn,flsql)
        ibm_db.bind_param(flstmt,1,fmail)
        ibm_db.bind_param(flstmt,2,fpass)
        ibm_db.execute(flstmt)
        facc = ibm_db.fetch_assoc(flstmt)
        if(facc):
            stat = facc['STATUS']
            status = stat.strip()
            print(status)
            if status == "Verified":
                session['fid']=facc['FID']
                session['fname']=facc['FNAME']
                session['fmail']=facc['FMAIL']
                session['floc']=facc['FLOCATION']
                userid = facc['FID']
                session['loggedin']=True
                return render_template('fhome.html')
            elif status == "Not Verified":
                msg1 = "Please wait until Admin verifies your Account"
            elif status == "Access Denied":
                msg1 = "Your Access is Denied by Management!"
            elif status == "Freezed":
                msg1 = "Your Account is Blocked,We'll Contact you soon"
            else:
                msg1 = "Please Try Again"
        else:
            msg1 = "Incorrect username/password"
        return render_template('login.html',msg1=msg1)

@app.route('/hlogin',methods=['GET','POST'])
def hlogin():
    global userid
    msg2=''
    if request.method == 'POST':
        hname = request.form['hemail']
        hpass = request.form['hpass']
        hlsql = "SELECT * FROM HOSTEL WHERE HMAIL = ? AND HPASSWORD = ?"
        hlstmt = ibm_db.prepare(conn,hlsql)
        ibm_db.bind_param(hlstmt,1,hname)
        ibm_db.bind_param(hlstmt,2,hpass)
        ibm_db.execute(hlstmt)
        hacc = ibm_db.fetch_assoc(hlstmt)
        if(hacc):
            stat = hacc['STATUS']
            status = stat.strip()
            if status == 'Verified':
                session['hid']=hacc['HID']
                session['hname']=hacc['HNAME']
                session['hloc']=hacc['HLOCATION']
                userid = hacc['HID']
                session['loggedin']=True
                return render_template('hhome.html')
            elif status == 'Not Verified':
                msg1 = "Please wait until Admin verifies your Account"
            elif status == "Access Denied":
                msg1 = "Your Access is Denied by Management!"
            elif status == "Freezed":
                msg1 = "Your Account is Blocked,We'll Contact you soon"
            else:
                msg1 = "Please Try Again"
        else:
            msg2 = "Incorrect email/password"
        return render_template('login.html',msg2=msg2)

@app.route('/freg',methods=['GET','POST'])
def freg():
    msg=''
    if request.method == 'POST':
        fname = request.form['fname']
        fmail = request.form['fmail']
        fph = request.form['fphone']
        floc = request.form['floc']
        fpass = request.form['fpass']
        fadd = request.form['fadd']
        frsql = "SELECT * FROM FARMERS WHERE FNAME =? AND FPHONE =? AND FMAIL = ?"
        frstmt = ibm_db.prepare(conn,frsql)
        ibm_db.bind_param(frstmt,1,fname)
        ibm_db.bind_param(frstmt,2,fph)
        ibm_db.bind_param(frstmt,3,fmail)
        ibm_db.execute(frstmt)
        facc = ibm_db.fetch_assoc(frstmt)
        if facc:
            msg = 'Account already exist!'
        elif not re.match(r'[A-Za-z0-9]+',fname):
            msg = 'Name must contain characters and number!'
        else:
            status = 'Not Verified'
            insql = "INSERT INTO FARMERS(FNAME,FPHONE,FPASSWORD,FLOCATION,FADDRESS,STATUS,FMAIL) VALUES(?,?,?,?,?,?,?)"
            instmt = ibm_db.prepare(conn,insql)
            ibm_db.bind_param(instmt,1,fname)
            ibm_db.bind_param(instmt,2,fph)
            ibm_db.bind_param(instmt,3,fpass)
            ibm_db.bind_param(instmt,4,floc)
            ibm_db.bind_param(instmt,5,fadd)
            ibm_db.bind_param(instmt,6,status)
            ibm_db.bind_param(instmt,7,fmail)
            ibm_db.execute(instmt)
            msg='you have successfully registered!Please Wait for Admin To Verify your Account.'
    return render_template('freg.html',msg=msg )

@app.route('/faccess')
def faccess():
    fsql = "SELECT * FROM FARMERS WHERE STATUS = ?"
    fstmt = ibm_db.prepare(conn,fsql)
    fstatus = 'Not Verified'
    ibm_db.bind_param(fstmt,1,fstatus)
    ibm_db.execute(fstmt)
    farm = ibm_db.fetch_assoc(fstmt)
    farmer=[]
    while farm:
        farmer.append(farm)
        farm = ibm_db.fetch_assoc(fstmt)
    return render_template('admin3.html',farmer=farmer)

@app.route('/fgrant/<fid>')
def fgrant(fid):
    status = "Verified"
    sql = "UPDATE FARMERS SET STATUS = ? WHERE FID = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,status)
    ibm_db.bind_param(stmt,2,fid)
    ibm_db.execute(stmt)
    fsql = "SELECT * FROM FARMERS WHERE STATUS = ?"
    fstmt = ibm_db.prepare(conn,fsql)
    fstatus = 'Not Verified'
    ibm_db.bind_param(fstmt,1,fstatus)
    ibm_db.execute(fstmt)
    farm = ibm_db.fetch_assoc(fstmt)
    farmer=[]
    while farm:
        farmer.append(farm)
        farm = ibm_db.fetch_assoc(fstmt)
    return render_template('admin3.html',farmer=farmer)

@app.route('/ffreeze/<fid>')
def ffreeze(fid):
    status = "Freezed"
    sql = "UPDATE FARMERS SET STATUS = ? WHERE FID = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,status)
    ibm_db.bind_param(stmt,2,fid)
    ibm_db.execute(stmt)
    fsql = "SELECT * FROM FARMERS WHERE STATUS = ?"
    fstmt = ibm_db.prepare(conn,fsql)
    fstatus = 'Verified'
    ibm_db.bind_param(fstmt,1,fstatus)
    ibm_db.execute(fstmt)
    farm = ibm_db.fetch_assoc(fstmt)
    farmer=[]
    while farm:
        farmer.append(farm)
        farm = ibm_db.fetch_assoc(fstmt)
    return render_template('admin5.html',farmer=farmer)  

@app.route('/funfreeze/<fid>')
def funfreeze(fid):
    status = "Verified"
    sql = "UPDATE FARMERS SET STATUS = ? WHERE FID = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,status)
    ibm_db.bind_param(stmt,2,fid)
    ibm_db.execute(stmt)
    fsql = "SELECT * FROM FARMERS WHERE STATUS = ?"
    fstmt = ibm_db.prepare(conn,fsql)
    fstatus = 'Verified'
    ibm_db.bind_param(fstmt,1,fstatus)
    ibm_db.execute(fstmt)
    farm = ibm_db.fetch_assoc(fstmt)
    farmer=[]
    while farm:
        farmer.append(farm)
        farm = ibm_db.fetch_assoc(fstmt)
    return render_template('admin5.html',farmer=farmer)

@app.route('/fraccounts')
def fraccounts():
    fsql = "SELECT * FROM FARMERS WHERE STATUS = ?"
    fstmt = ibm_db.prepare(conn,fsql)
    fstatus = 'Freezed'
    ibm_db.bind_param(fstmt,1,fstatus)
    ibm_db.execute(fstmt)
    farm = ibm_db.fetch_assoc(fstmt)
    farmer=[]
    while farm:
        farmer.append(farm)
        farm = ibm_db.fetch_assoc(fstmt)
    hsql = "SELECT * FROM HOSTEL WHERE STATUS = ?"
    hstmt = ibm_db.prepare(conn,hsql)
    hstatus = 'Freezed'
    ibm_db.bind_param(hstmt,1,hstatus)
    ibm_db.execute(hstmt)
    host = ibm_db.fetch_assoc(hstmt)
    hostel=[]
    while host:
        hostel.append(host)
        host = ibm_db.fetch_assoc(hstmt)
    return render_template('admin7.html',farmer = farmer,hostel = hostel)

@app.route('/fdeny/<fid>')
def fdeny(fid):
    status = "Access Denied"
    sql = "UPDATE FARMERS SET STATUS = ? WHERE FID = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,status)
    ibm_db.bind_param(stmt,2,fid)
    ibm_db.execute(stmt)
    fsql = "SELECT * FROM FARMERS WHERE STATUS = ?"
    fstmt = ibm_db.prepare(conn,fsql)
    fstatus = 'Not Verified'
    ibm_db.bind_param(fstmt,1,fstatus)
    ibm_db.execute(fstmt)
    farm = ibm_db.fetch_assoc(fstmt)
    farmer=[]
    while farm:
        farmer.append(farm)
        farm = ibm_db.fetch_assoc(fstmt)
    return render_template('admin3.html',farmer=farmer)

@app.route('/fprofile')
def profile():
    fid = session['fid']
    sql = "SELECT * FROM FARMERS WHERE FID = ?"
    st = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(st,1,fid)
    ibm_db.execute(st)
    f = ibm_db.fetch_assoc(st)
    name=f['FNAME']
    ph = f['FPHONE']
    loc = f['FLOCATION']
    add = f['FADDRESS']
    mail =f['FMAIL']
    return render_template('fprofile.html',name=name,loc=loc,ph=ph,add=add,mail=mail)

@app.route('/fconfirm/<oid>')
def fconfirm(oid):
    consql = "UPDATE ORDER SET STATUS = 'Delivered by Farmer' WHERE OID = ?"
    constmt = ibm_db.prepare(conn,consql)
    ibm_db.bind_param(constmt,1,oid)
    ibm_db.execute(constmt)
    fid = session['fid']
    fosql = "SELECT * FROM ORDER WHERE FID = ? AND (STATUS = 'Yet to deliver' OR STATUS = 'Confirmed by Farmer')"
    fostmt = ibm_db.prepare(conn,fosql)
    ibm_db.bind_param(fostmt,1,fid)
    ibm_db.execute(fostmt)
    order = ibm_db.fetch_assoc(fostmt)
    forders = []
    while order:
        hid = order['HID']
        pid = order['PID']
        psql  = "SELECT * FROM PRODUCT WHERE PID = ?"
        pstmt = ibm_db.prepare(conn,psql)
        ibm_db.bind_param(pstmt,1,pid)
        ibm_db.execute(pstmt)
        pro = ibm_db.fetch_assoc(pstmt)
        order['NAME'] = pro['PNAME']
        hsql = "SELECT * FROM HOSTEL WHERE HID = ?"
        hstmt = ibm_db.prepare(conn,hsql)
        ibm_db.bind_param(hstmt,1,hid)
        ibm_db.execute(hstmt)
        hostel = ibm_db.fetch_assoc(hstmt)
        order['HNAME'] = hostel['HNAME']
        order['HPH'] = hostel['HPHONE']
        order['HADD'] = hostel['HADDRESS']
        forders.append(order)
        order = ibm_db.fetch_assoc(fostmt)
    
    fhsql = "SELECT * FROM ORDER WHERE FID = ? AND NOT (STATUS = 'Yet to deliver' OR STATUS = 'Delivered by Farmer' OR STATUS = 'Confirmed by Farmer') ORDER BY TIME DESC"
    fhstmt = ibm_db.prepare(conn,fhsql)
    ibm_db.bind_param(fhstmt,1,fid)
    ibm_db.execute(fhstmt)
    horder = ibm_db.fetch_assoc(fhstmt)
    fhorders = []
    while horder:
        hid = horder['HID']
        pid = horder['PID']
        psql  = "SELECT * FROM PRODUCT WHERE PID = ?"
        pstmt = ibm_db.prepare(conn,psql)
        ibm_db.bind_param(pstmt,1,pid)
        ibm_db.execute(pstmt)
        pro = ibm_db.fetch_assoc(pstmt)
        horder['NAME'] = pro['PNAME']
        hsql = "SELECT * FROM HOSTEL WHERE HID = ?"
        hstmt = ibm_db.prepare(conn,hsql)
        ibm_db.bind_param(hstmt,1,hid)
        ibm_db.execute(hstmt)
        hostel = ibm_db.fetch_assoc(hstmt)
        horder['HNAME'] = hostel['HNAME']
        horder['HPH'] = hostel['HPHONE']
        horder['HADD'] = hostel['HADDRESS']
        fhorders.append(horder)
        horder = ibm_db.fetch_assoc(fostmt)
    return render_template('forders.html',order = forders,orderh=fhorders)


@app.route('/fedit',methods=['GET','POST'])
def fedit():
    fid = session['fid']
    if request.method == 'POST':
        fname = request.form['fname']
        fph = request.form['fphone']
        floc = request.form['floc']
        fadd = request.form['fadd']
        fmail = request.form['fmail']
        fsql = "UPDATE FARMERS SET FNAME=?,FPHONE = ?,FLOCATION=?,FADDRESS = ?,FMAIL= ? WHERE FID = ?"
        fstmt = ibm_db.prepare(conn,fsql)
        ibm_db.bind_param(fstmt,1,fname)
        ibm_db.bind_param(fstmt,2,fph)
        ibm_db.bind_param(fstmt,3,floc)
        ibm_db.bind_param(fstmt,4,fadd)
        ibm_db.bind_param(fstmt,5,fmail)
        ibm_db.bind_param(fstmt,6,fid)
        ibm_db.execute(fstmt)
        return render_template('fprofile.html',name=fname,ph=fph,loc=floc,add=fadd,mail =fmail)
    
@app.route('/alogin')
def alogin():
    msg1= ""
    return render_template('alogin.html',msg1=msg1)

@app.route('/ahome')
def ahome():
    rsql = "SELECT * FROM REPORT WHERE STATUS LIKE 'Reported%'"
    rstmt = ibm_db.prepare(conn,rsql)
    ibm_db.execute(rstmt)
    farm = ibm_db.fetch_assoc(rstmt)
    farmer = []
    print(farm)
    while farm:
        farmer.append(farm)
        farm = ibm_db.fetch_assoc(rstmt)
    print(farmer)
    return render_template('admin.html',farmer=farmer)

@app.route('/rhistory')
def rhistory():
    rsql = "SELECT * FROM REPORT WHERE STATUS NOT LIKE 'Reported%'"
    rstmt = ibm_db.prepare(conn,rsql)
    ibm_db.execute(rstmt)
    farm = ibm_db.fetch_assoc(rstmt)
    farmer = []
    while farm:
        farmer.append(farm)
        farm = ibm_db.fetch_assoc(rstmt)
    print(farmer)
    return render_template('admin2.html',farmer=farmer)


@app.route('/admin',methods = ['GET','POST'])
def admin():

    if request.method == "POST":
        name = request.form['aname']
        password = request.form['apass'] 
        sql = "SELECT * FROM ADMIN WHERE NAME = ? AND PASSWORK = ?"
        st = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(st,1,name)
        ibm_db.bind_param(st,2,password)
        ibm_db.execute(st)
        a = ibm_db.fetch_assoc(st)
        if a:
            rsql = "SELECT * FROM REPORT WHERE  STATUS LIKE 'Reported%'"
            rstmt = ibm_db.prepare(conn,rsql)
            ibm_db.execute(rstmt)
            farm = ibm_db.fetch_assoc(rstmt)
            farmer = []
            while farm:
                farmer.append(farm)
                farm = ibm_db.fetch_assoc(rstmt)
            return render_template('admin.html',farmer=farmer)
        else:
            msg = "Incorrect Username/Password"
        return render_template('alogin.html',msg1=msg)

@app.route('/solved/<rid>')
def solved(rid):
    sql = "UPDATE REPORT SET STATUS = 'Solved' WHERE RID = ?"
    st = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(st,1,rid)
    ibm_db.execute(st)
    rsql = "SELECT * FROM REPORT WHERE STATUS LIKE 'Reported%'"
    rstmt = ibm_db.prepare(conn,rsql)
    ibm_db.execute(rstmt)
    farm = ibm_db.fetch_assoc(rstmt)
    farmer = []
    while farm:
        farmer.append(farm)
        farm = ibm_db.fetch_assoc(rstmt)
    return render_template('admin.html',farmer=farmer)

@app.route('/alogout')
def alogout():
    return render_template('login.html')

@app.route('/hreg',methods=['GET','POST'])
def href():
    msg=''
    if request.method == 'POST':
        hname = request.form['hname']
        hmail = request.form['hmail']
        hph = request.form['hphone']
        hloc = request.form['hloc']
        hadd = request.form['hadd']
        hpass = request.form['hpass']
        hrsql = "SELECT * FROM HOSTEL WHERE HNAME = ? AND HMAIL =?"
        hrstmt = ibm_db.prepare(conn,hrsql)
        ibm_db.bind_param(hrstmt,1,hname)
        ibm_db.bind_param(hrstmt,2,hmail)
        ibm_db.execute(hrstmt)
        hacc = ibm_db.fetch_assoc(hrstmt)
        if hacc:
            msg = "Account Already exist!"
        else:
            status = 'Not Verified'
            insql = "INSERT INTO HOSTEL(HNAME,HPHONE,HMAIL,HPASSWORD,HLOCATION,HADDRESS,STATUS) VALUES(?,?,?,?,?,?,?)"
            instmt = ibm_db.prepare(conn,insql)
            ibm_db.bind_param(instmt,1,hname)
            ibm_db.bind_param(instmt,2,hph)
            ibm_db.bind_param(instmt,3,hmail)
            ibm_db.bind_param(instmt,4,hpass)
            ibm_db.bind_param(instmt,5,hloc)
            ibm_db.bind_param(instmt,6,hadd)
            ibm_db.bind_param(instmt,7,status)
            ibm_db.execute(instmt)
            msg = 'you have successfully registered!, Please wait for admin to verify your account'
    return render_template('hreg.html',msg = msg)

@app.route('/afarmer')
def afarmer():
    status = "Verified"
    fsql = "SELECT * FROM FARMERS WHERE STATUS = ?"
    fstmt = ibm_db.prepare(conn,fsql)
    ibm_db.bind_param(fstmt,1,status)
    ibm_db.execute(fstmt)
    farm = ibm_db.fetch_assoc(fstmt)
    farmer=[]
    while farm:
        farmer.append(farm)
        farm = ibm_db.fetch_assoc(fstmt)
    return render_template('admin5.html',farmer=farmer)

@app.route('/ahostel')
def ahostel():
    hsql = "SELECT * FROM HOSTEL WHERE STATUS = ?"
    hstmt = ibm_db.prepare(conn,hsql)
    hstatus = 'Verified'
    ibm_db.bind_param(hstmt,1,hstatus)
    ibm_db.execute(hstmt)
    host = ibm_db.fetch_assoc(hstmt)
    hostel=[]
    while host:
        hostel.append(host)
        host = ibm_db.fetch_assoc(hstmt)
    return render_template('admin6.html',hostel=hostel)

@app.route('/haccess')
def haccess():
    hsql = "SELECT * FROM HOSTEL WHERE STATUS = ?"
    hstmt = ibm_db.prepare(conn,hsql)
    hstatus = 'Not Verified'
    ibm_db.bind_param(hstmt,1,hstatus)
    ibm_db.execute(hstmt)
    host = ibm_db.fetch_assoc(hstmt)
    hostel=[]
    while host:
        hostel.append(host)
        host = ibm_db.fetch_assoc(hstmt)
    return render_template('admin4.html',hostel=hostel)

@app.route('/hfreeze/<hid>')
def hfreeze(hid):
    status = "Freezed"
    sql = "UPDATE HOSTEL SET STATUS = ? WHERE HID = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,status)
    ibm_db.bind_param(stmt,2,hid)
    ibm_db.execute(stmt)
    hsql = "SELECT * FROM HOSTEL WHERE STATUS = ?"
    hstmt = ibm_db.prepare(conn,hsql)
    hstatus = 'Verified'
    ibm_db.bind_param(hstmt,1,hstatus)
    ibm_db.execute(hstmt)
    host = ibm_db.fetch_assoc(hstmt)
    hostel=[]
    while host:
        hostel.append(host)
        host = ibm_db.fetch_assoc(hstmt)
    return render_template('admin6.html',hostel=hostel)

@app.route('/hunfreeze/<hid>')
def hunfreeze(hid):
    status = "Verified"
    sql = "UPDATE HOSTEL SET STATUS = ? WHERE HID = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,status)
    ibm_db.bind_param(stmt,2,hid)
    ibm_db.execute(stmt)
    hsql = "SELECT * FROM HOSTEL WHERE STATUS = ?"
    hstmt = ibm_db.prepare(conn,hsql)
    hstatus = 'Verified'
    ibm_db.bind_param(hstmt,1,hstatus)
    ibm_db.execute(hstmt)
    host = ibm_db.fetch_assoc(hstmt)
    hostel=[]
    while host:
        hostel.append(host)
        host = ibm_db.fetch_assoc(hstmt)
    return render_template('admin6.html',hostel=hostel)

@app.route('/hgrant/<hid>')
def hgrant(hid):
    status = "Verified"
    sql = "UPDATE HOSTEL SET STATUS = ? WHERE HID = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,status)
    ibm_db.bind_param(stmt,2,hid)
    ibm_db.execute(stmt)
    hsql = "SELECT * FROM HOSTEL WHERE STATUS = ?"
    hstmt = ibm_db.prepare(conn,hsql)
    hstatus = 'Not Verified'
    ibm_db.bind_param(hstmt,1,hstatus)
    ibm_db.execute(hstmt)
    host = ibm_db.fetch_assoc(hstmt)
    hostel=[]
    while host:
        hostel.append(host)
        host = ibm_db.fetch_assoc(hstmt)
    return render_template('admin4.html',hostel=hostel)

@app.route('/hdeny/<hid>')
def hdeny(hid):
    status = "Access Denied"
    sql = "UPDATE HOSTEL SET STATUS = ? WHERE HID = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,status)
    ibm_db.bind_param(stmt,2,hid)
    ibm_db.execute(stmt)
    hsql = "SELECT * FROM HOSTEL WHERE STATUS = ?"
    hstmt = ibm_db.prepare(conn,hsql)
    hstatus = 'Not Verified'
    ibm_db.bind_param(hstmt,1,hstatus)
    ibm_db.execute(hstmt)
    host = ibm_db.fetch_assoc(hstmt)
    hostel=[]
    while host:
        hostel.append(host)
        host = ibm_db.fetch_assoc(hstmt)
    return render_template('admin4.html',hostel=hostel)

@app.route('/hprofile')
def fprofile():
    hid = session['hid']
    sql = "SELECT * FROM HOSTEL WHERE HID = ?"
    st = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(st,1,hid)
    ibm_db.execute(st)
    h= ibm_db.fetch_assoc(st)
    name = h['HNAME']
    email = h['HMAIL']
    loc = h['HLOCATION']
    ph = h['HPHONE']
    add = h['HADDRESS']
    return render_template('hprofile.html',name=name,email=email,loc=loc,ph=ph,add=add)

@app.route('/hedit',methods=['GET','POST'])
def hedit():
    hid = session['hid']
    if request.method == 'POST':
        hname = request.form['hname']
        hmail = request.form['hmail']
        hph = request.form['hphone']
        hloc = request.form['hloc']
        hadd = request.form['hadd']
        sql = "UPDATE HOSTEL SET HNAME = ?,HMAIL = ?,HLOCATION = ?,HPHONE = ?,HADDRESS = ? WHERE HID = ?"
        st = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(st,1,hname)
        ibm_db.bind_param(st,2,hmail)
        ibm_db.bind_param(st,3,hloc)
        ibm_db.bind_param(st,4,hph)
        ibm_db.bind_param(st,5,hadd)
        ibm_db.bind_param(st,6,hid)
        ibm_db.execute(st)
        return render_template('hprofile.html',name=hname,email=hmail,loc=hloc,ph=hph,add=hadd)


@app.route('/fhome')
def fhome():
    return render_template('fhome.html')

@app.route('/hhome')
def hhome():
    return render_template('hhome.html')

@app.route('/hadmin')
def hadmin():
    return render_template('hreport.html')

@app.route('/hrep',methods=['GET','POST'])
def hrep():
    hid = session['hid']
    msg = ""
    if request.method == 'POST':
        user = "hostel"
        name = request.form['name']
        ph = request.form['ph']
        problem = request.form['problem']
        desc = request.form['desc']
        status = "Reported"
        sql = "INSERT INTO REPORT(USER,ID,NAME,PROBLEM,EXP,PHONE,STATUS) VALUES(?,?,?,?,?,?,?)"
        st = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(st,1,user)
        ibm_db.bind_param(st,2,hid)
        ibm_db.bind_param(st,3,name)
        ibm_db.bind_param(st,4,problem)
        ibm_db.bind_param(st,5,desc)
        ibm_db.bind_param(st,6,ph)
        ibm_db.bind_param(st,7,status)
        ibm_db.execute(st)
        msg = "your Report Submitted successfully"
    return render_template('hreport.html',msg = msg)

@app.route('/fadmin')
def fadmin():
    return render_template('freport.html')

@app.route('/frep',methods=['GET','POST'])
def frep():
    fid = session['fid']
    msg = ""
    if request.method == 'POST':
        user = "farmer"
        name = request.form['name']
        ph = request.form['ph']
        problem = request.form['problem']
        desc = request.form['desc']
        status = "Reported"
        sql = "INSERT INTO REPORT(USER,ID,NAME,PROBLEM,EXP,PHONE,STATUS) VALUES(?,?,?,?,?,?,?)"
        st = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(st,1,user)
        ibm_db.bind_param(st,2,fid)
        ibm_db.bind_param(st,3,name)
        ibm_db.bind_param(st,4,problem)
        ibm_db.bind_param(st,5,desc)
        ibm_db.bind_param(st,6,ph)
        ibm_db.bind_param(st,7,status)
        ibm_db.execute(st)
        msg = "your Report Submitted successfully"
    return render_template('freport.html',msg = msg)

@app.route('/fpro')
def fpro():
    id=session['fid']
    print(id)
    psql = "SELECT * FROM PRODUCT WHERE FID = ?"
    pstmt = ibm_db.prepare(conn,psql)
    ibm_db.bind_param(pstmt,1,id)
    ibm_db.execute(pstmt)
    pro = ibm_db.fetch_assoc(pstmt)
    fpro = []
    while pro:
        fpro.append(pro)
        pro = ibm_db.fetch_assoc(pstmt)
    msg = 'Upload your product here'
    return render_template('fproduct.html',msg=msg,pro=fpro)

@app.route('/proupt',methods=['GET','POST'])
def proupt():
    msg = ''
    fid = session['fid']
    if request.method=='POST':
        pname = request.form['pname']
        price = request.form['pprice']
        pgrade = request.form['pgrade']
        print(pgrade)
        pq = request.form['pq']
        psql = "SELECT * FROM PRODUCT WHERE FID = ? AND PNAME = ? AND GRADE = ?"
        pstmt = ibm_db.prepare(conn,psql)
        ibm_db.bind_param(pstmt,1,fid)
        ibm_db.bind_param(pstmt,2,pname)
        ibm_db.bind_param(pstmt,3,pgrade)
        ibm_db.execute(pstmt)
        fa = ibm_db.fetch_assoc(pstmt)
        if fa:
            pu = "UPDATE PRODUCT SET PRICE = ? ,PQUANTITY = ? WHERE FID = ? AND PNAME = ? AND GRADE = ?"
            ps =ibm_db.prepare(conn,pu)
            ibm_db.bind_param(ps,1,price)
            ibm_db.bind_param(ps,2,pq)
            ibm_db.bind_param(ps,3,fid)
            ibm_db.bind_param(ps,4,pname)
            ibm_db.bind_param(ps,5,pgrade)
            ibm_db.execute(ps)
            msg="Product Successfully Updated"
        else:
            pu ="INSERT INTO PRODUCT(PNAME,PRICE,PQUANTITY,FID,GRADE) VALUES(?,?,?,?,?)"
            ps =ibm_db.prepare(conn,pu)
            ibm_db.bind_param(ps,1,pname)
            ibm_db.bind_param(ps,2,price)
            ibm_db.bind_param(ps,3,pq)
            ibm_db.bind_param(ps,4,fid)
            ibm_db.bind_param(ps,5,pgrade)
            ibm_db.execute(ps)
            msg ="Product Successfully Uploaded"
    
    print(msg)
    psql = "SELECT * FROM PRODUCT WHERE FID = ?"
    pstmt = ibm_db.prepare(conn,psql)
    ibm_db.bind_param(pstmt,1,fid)
    ibm_db.execute(pstmt)
    pro = ibm_db.fetch_assoc(pstmt)
    fpro = []
    while pro:
        fpro.append(pro)
        pro = ibm_db.fetch_assoc(pstmt)
    return render_template('fproduct.html',msg=msg,pro = fpro)

@app.route('/remove/<pid>')
def remove(pid):
    sql = "DELETE FROM PRODUCT WHERE PID = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,pid)
    ibm_db.execute(stmt)
    fid = session['fid']
    psql = "SELECT * FROM PRODUCT WHERE FID = ?"
    pstmt = ibm_db.prepare(conn,psql)
    ibm_db.bind_param(pstmt,1,fid)
    ibm_db.execute(pstmt)
    pro = ibm_db.fetch_assoc(pstmt)
    fpro = []
    while pro:
        fpro.append(pro)
        pro = ibm_db.fetch_assoc(pstmt)
    return render_template('fproduct.html',msg ="",pro = fpro)

@app.route('/hshop')
def shop():
    hloc = session['hloc']
    fsql = "SELECT FID FROM FARMERS WHERE FLOCATION = ? AND STATUS = 'Verified' "
    fstmt = ibm_db.prepare(conn,fsql)
    ibm_db.bind_param(fstmt,1,hloc)
    ibm_db.execute(fstmt)
    fids = ibm_db.fetch_assoc(fstmt)
    fid = []
    while fids:
        fid.append(fids)
        fids = ibm_db.fetch_assoc(fstmt)
    pro =[]
    for i in fid:
        for j in i.values():
            id = j
            psql = "SELECT * FROM PRODUCT WHERE FID =? "
            pstmt = ibm_db.prepare(conn,psql)
            ibm_db.bind_param(pstmt,1,id)
            ibm_db.execute(pstmt)
            fpro =ibm_db.fetch_assoc(pstmt)
            while fpro:
                #getffpro['pname] and get the image and append it to fpro
                rate = int(fpro['RATING'])
                fpro['rate'] = rate
                nm = fpro['PNAME']
                grade=fpro['GRADE']
                faid = fpro['FID']
                isql = "SELECT * FROM IMAGE WHERE NAME = ? AND GRADE=?"
                istmt = ibm_db.prepare(conn,isql)
                ibm_db.bind_param(istmt,1,nm)
                ibm_db.bind_param(istmt,2,grade)
                ibm_db.execute(istmt)
                im = ibm_db.fetch_assoc(istmt)
                iname = im['INAME']
                fpro['INAME'] = iname
                fnsql = "SELECT FNAME,FLOCATION FROM FARMERS WHERE FID = ?"
                fnstmt = ibm_db.prepare(conn,fnsql)
                ibm_db.bind_param(fnstmt,1,faid)
                ibm_db.execute(fnstmt)
                fna = ibm_db.fetch_assoc(fnstmt)
                fname = fna['FNAME']
                fpro['FNAME'] = fname
                fpro['FLOCATION'] = fna['FLOCATION']
                pro.append(fpro)
                fpro = ibm_db.fetch_assoc(pstmt)
    lsql = "SELECT DISTINCT FLOCATION FROM FARMERS"
    lstmt = ibm_db.prepare(conn,lsql)
    ibm_db.execute(lstmt)
    loc = ibm_db.fetch_assoc(lstmt)
    location = []
    while loc:
        location.append(loc)
        loc = ibm_db.fetch_assoc(lstmt)
    print(loc)
    return render_template('hshop.html',hloc=hloc,pro=pro,loc=location)

@app.route('/psearch',methods = ['GET','POST'])
def psearch():
    if request.method == 'POST':
        pname = request.form['pname']
        grade = request.form['grade']
        price = request.form['price']
        product = []
        if price == 'High to Low':
            sql = "SELECT * FROM PRODUCT WHERE PNAME = ? AND GRADE = ?"
            st = ibm_db.prepare(conn,sql)
            ibm_db.bind_param(st,1,pname)
            ibm_db.bind_param(st,2,grade)
            ibm_db.execute(st)
            pro = ibm_db.fetch_assoc(st)
            while pro:
                rate = int(pro['RATING'])
                pro['rate'] = rate
                nm = pro['PNAME']
                faid = pro['FID']
                isql = "SELECT * FROM IMAGE WHERE NAME = ? AND GRADE=?"
                istmt = ibm_db.prepare(conn,isql)
                ibm_db.bind_param(istmt,1,nm)
                ibm_db.bind_param(istmt,2,grade)
                ibm_db.execute(istmt)
                im = ibm_db.fetch_assoc(istmt)
                iname = im['INAME']
                pro['INAME'] = iname
                fnsql = "SELECT FNAME,FLOCATION FROM FARMERS WHERE FID = ?"
                fnstmt = ibm_db.prepare(conn,fnsql)
                ibm_db.bind_param(fnstmt,1,faid)
                ibm_db.execute(fnstmt)
                fna = ibm_db.fetch_assoc(fnstmt)
                fname = fna['FNAME']
                pro['FNAME'] = fname
                pro['FLOCATION'] = fna['FLOCATION']
                product.append(pro)
                pro = ibm_db.fetch_assoc(st)
        else:
            sql = "SELECT * FROM PRODUCT WHERE PNAME = ? AND GRADE = ?"
            st = ibm_db.prepare(conn,sql)
            ibm_db.bind_param(st,1,pname)
            ibm_db.bind_param(st,2,grade)
            ibm_db.execute(st)
            pro = ibm_db.fetch_assoc(st)
            while pro:
                rate = int(pro['RATING'])
                pro['rate'] = rate
                nm = pro['PNAME']
                faid = pro['FID']
                isql = "SELECT * FROM IMAGE WHERE NAME = ? AND GRADE=?"
                istmt = ibm_db.prepare(conn,isql)
                ibm_db.bind_param(istmt,1,nm)
                ibm_db.bind_param(istmt,2,grade)
                ibm_db.execute(istmt)
                im = ibm_db.fetch_assoc(istmt)
                iname = im['INAME']
                pro['INAME'] = iname
                fnsql = "SELECT FNAME,FLOCATION FROM FARMERS WHERE FID = ?"
                fnstmt = ibm_db.prepare(conn,fnsql)
                ibm_db.bind_param(fnstmt,1,faid)
                ibm_db.execute(fnstmt)
                fna = ibm_db.fetch_assoc(fnstmt)
                fname = fna['FNAME']
                pro['FNAME'] = fname
                pro['FLOCATION'] = fna['FLOCATION']
                product.append(pro)
                pro = ibm_db.fetch_assoc(st)
    lsql = "SELECT DISTINCT FLOCATION FROM FARMERS"
    lstmt = ibm_db.prepare(conn,lsql)
    ibm_db.execute(lstmt)
    loc = ibm_db.fetch_assoc(lstmt)
    location = []
    while loc:
        location.append(loc)
        loc = ibm_db.fetch_assoc(lstmt)
    print(loc)
    return render_template('hshop.html',hloc='',pro=product,loc=location)

@app.route('/pfilter',methods=['GET','POST'])
def filter():
        ploc = request.form['location']
        fsql = "SELECT FID FROM FARMERS WHERE FLOCATION = ? AND STATUS = 'Verified'"
        fstmt = ibm_db.prepare(conn,fsql)
        ibm_db.bind_param(fstmt,1,ploc)
        ibm_db.execute(fstmt)
        fids = ibm_db.fetch_assoc(fstmt)
        fid = []
        while fids:
            fid.append(fids)
            fids = ibm_db.fetch_assoc(fstmt)
        pro =[]
        for i in fid:
            for j in i.values():
                id = j
                psql = "SELECT * FROM PRODUCT WHERE FID =?"
                pstmt = ibm_db.prepare(conn,psql)
                ibm_db.bind_param(pstmt,1,id)
                ibm_db.execute(pstmt)
                fpro =ibm_db.fetch_assoc(pstmt)
                while fpro:
                    rate = int(fpro['RATING'])
                    fpro['rate'] = rate
                    nm = fpro['PNAME']
                    faid = fpro['FID']
                    grade = fpro['GRADE']
                    isql = "SELECT * FROM IMAGE WHERE NAME = ? AND GRADE =?"
                    istmt = ibm_db.prepare(conn,isql)
                    ibm_db.bind_param(istmt,1,nm)
                    ibm_db.bind_param(istmt,2,grade)
                    ibm_db.execute(istmt)
                    im = ibm_db.fetch_assoc(istmt)
                    iname = im['INAME']
                    fpro['INAME'] = iname
                    fnsql = "SELECT FNAME,FLOCATION FROM FARMERS WHERE FID = ?"
                    fnstmt = ibm_db.prepare(conn,fnsql)
                    ibm_db.bind_param(fnstmt,1,faid)
                    ibm_db.execute(fnstmt)
                    fna = ibm_db.fetch_assoc(fnstmt)
                    fname = fna['FNAME']
                    fpro['FNAME'] = fname
                    fpro['FLOCATION'] = fna['FLOCATION']
                    pro.append(fpro)
                    fpro = ibm_db.fetch_assoc(pstmt)
        lsql = "SELECT DISTINCT FLOCATION FROM FARMERS WHERE STATUS = 'Verified'"
        lstmt = ibm_db.prepare(conn,lsql)
        ibm_db.execute(lstmt)
        loc = ibm_db.fetch_assoc(lstmt)
        location = []
        while loc:
            location.append(loc)
            loc = ibm_db.fetch_assoc(lstmt) 
        return render_template('hshop.html',hloc=ploc,pro=pro,loc = location)

@app.route('/shop/<pid>')
def pshop(pid):
    psql = "SELECT * FROM PRODUCT WHERE PID = ?"
    pstmt = ibm_db.prepare(conn,psql)
    ibm_db.bind_param(pstmt,1,pid)
    ibm_db.execute(pstmt)
    pr = ibm_db.fetch_assoc(pstmt)
    pname = pr['PNAME']
    pgrade = pr['GRADE']
    price = pr['PRICE']
    pq = pr['PQUANTITY']
    fid = pr['FID']
    rate = int(pr['RATING'])
    norate = pr['NORATE']
    fsql = "SELECT FNAME,FLOCATION FROM FARMERS WHERE FID = ?"
    fstmt = ibm_db.prepare(conn,fsql)
    ibm_db.bind_param(fstmt,1,fid)
    ibm_db.execute(fstmt)
    fn = ibm_db.fetch_assoc(fstmt)
    fname = fn['FNAME']
    floc = fn['FLOCATION']
    isql = "SELECT * FROM IMAGE WHERE NAME = ? AND GRADE = ?"
    istmt = ibm_db.prepare(conn,isql)
    ibm_db.bind_param(istmt,1,pname)
    ibm_db.bind_param(istmt,2,pgrade)
    ibm_db.execute(istmt)
    image = ibm_db.fetch_assoc(istmt)
    img = image['INAME']
    return render_template('hpro.html',rate=rate,norate=norate,pname=pname,pid=pid,price=price,pq=pq,fname=fname,floc=floc,img=img,pgrade = pgrade)

@app.route('/buy/<pid>',methods=['GET','POST'])
def buy(pid):
    if request.method == 'POST':
        oq = request.form['quantity']
        psql = "SELECT * FROM PRODUCT WHERE PID = ?"
        pstmt = ibm_db.prepare(conn,psql)
        ibm_db.bind_param(pstmt,1,pid)
        ibm_db.execute(pstmt)
        p = ibm_db.fetch_assoc(pstmt)
        pname = p['PNAME']
        price = p['PRICE']
        hid = session['hid']
        hsql = "SELECT * FROM HOSTEL WHERE HID = ?"
        hstmt = ibm_db.prepare(conn,hsql)
        ibm_db.bind_param(hstmt,1,hid)
        ibm_db.execute(hstmt)
        h = ibm_db.fetch_assoc(hstmt)
        hname = h['HNAME']
        hphone = h['HPHONE']
        hmail = h['HMAIL']
        hadd = h['HADDRESS']
        pin =h['PINCODE']
        pr = float(price) * float(oq)
        return render_template('placeorder.html',pid=pid,hname=hname,hphone=hphone,hmail=hmail,address=hadd,price=price,pname=pname,oq=oq,tp=pr,pc=pin)

@app.route('/pbuy')
def pbuy():
    hid =session['hid']
    pid = request.args.get('arg1')
    oq = request.args.get('arg2')
    psql = "SELECT * FROM PRODUCT WHERE PID = ?"
    pstmt= ibm_db.prepare(conn,psql)
    ibm_db.bind_param(pstmt,1,pid)
    ibm_db.execute(pstmt)
    p = ibm_db.fetch_assoc(pstmt)
    fid = p['FID']
    print(fid)
    price = p['PRICE']
    quantity= p['PQUANTITY']

    pq = float(quantity) - float(oq)
    pqsql = "UPDATE PRODUCT SET PQUANTITY = ? WHERE PID = ?"
    pqstmt = ibm_db.prepare(conn,pqsql)
    ibm_db.bind_param(pqstmt,1,pq)
    ibm_db.bind_param(pqstmt,2,pid)
    ibm_db.execute(pqstmt)
    price = float(price) * float(oq)
    status = 'Yet to deliver'
    time = datetime.now()
    osql = "INSERT INTO ORDER(PID,FID,HID,OQUANTITY,PRICE,STATUS,TIME) VALUES(?,?,?,?,?,?,?)"
    ostmt = ibm_db.prepare(conn,osql)
    ibm_db.bind_param(ostmt,1,pid)
    ibm_db.bind_param(ostmt,2,fid)
    ibm_db.bind_param(ostmt,3,hid),
    ibm_db.bind_param(ostmt,4,oq)
    ibm_db.bind_param(ostmt,5,price)
    ibm_db.bind_param(ostmt,6,status)
    ibm_db.bind_param(ostmt,7,time)
    ibm_db.execute(ostmt)
    
    orsql="SELECT * FROM ORDER WHERE HID = ? AND STATUS = 'Yet to deliver'"
    orstmt = ibm_db.prepare(conn,orsql)
    ibm_db.bind_param(orstmt,1,hid)
    ibm_db.execute(orstmt)
    o = ibm_db.fetch_assoc(orstmt)
    orders = []
    while o:
        proid = o['PID']
        productsql = "SELECT * FROM PRODUCT WHERE PID = ?"
        prostmt = ibm_db.prepare(conn,productsql)
        ibm_db.bind_param(prostmt,1,proid)
        ibm_db.execute(prostmt)
        product = ibm_db.fetch_assoc(prostmt)
        productname = product['PNAME']
        o['NAME'] = productname 
        farid = o['FID']
        farmsql = "SELECT * FROM FARMERS WHERE FID = ?"
        farmstmt = ibm_db.prepare(conn,farmsql)
        ibm_db.bind_param(farmstmt,1,farid)
        ibm_db.execute(farmstmt)
        farm = ibm_db.fetch_assoc(farmstmt)
        o['FNAME'] = farm['FNAME']
        o['FPH'] = farm['FPHONE']
        orders.append(o)
        o = ibm_db.fetch_assoc(orstmt)
    
    hsql="SELECT * FROM ORDER WHERE HID = ? AND NOT (STATUS = 'Yet to deliver' OR STATUS = 'Confirmed by Farmer') ORDER BY TIME DESC"
    hstmt = ibm_db.prepare(conn,hsql)
    ibm_db.bind_param(hstmt,1,hid)
    ibm_db.execute(hstmt)
    h = ibm_db.fetch_assoc(hstmt)
    orderh = []
    while h:
        proid = h['PID']
        productsql = "SELECT * FROM PRODUCT WHERE PID = ?"
        prostmt = ibm_db.prepare(conn,productsql)
        ibm_db.bind_param(prostmt,1,proid)
        ibm_db.execute(prostmt)
        product = ibm_db.fetch_assoc(prostmt)
        productname = product['PNAME']
        h['NAME'] = productname 
        farid = h['FID']
        farmsql = "SELECT * FROM FARMERS WHERE FID = ?"
        farmstmt = ibm_db.prepare(conn,farmsql)
        ibm_db.bind_param(farmstmt,1,farid)
        ibm_db.execute(farmstmt)
        farm = ibm_db.fetch_assoc(farmstmt)
        h['FNAME'] = farm['FNAME']
        h['FPH'] = farm['FPHONE']
        orderh.append(h)
        h = ibm_db.fetch_assoc(hstmt)
    return render_template('horder.html',order = orders,orderh=orderh)

@app.route('/horder')
def horder():
    hid = session['hid']
    orsql="SELECT * FROM ORDER WHERE HID = ? AND (STATUS = 'Yet to deliver' OR STATUS = 'Confirmed by Farmer')"
    orstmt = ibm_db.prepare(conn,orsql)
    ibm_db.bind_param(orstmt,1,hid)
    ibm_db.execute(orstmt)
    o = ibm_db.fetch_assoc(orstmt)
    orders = []
    while o:
        proid = o['PID']
        productsql = "SELECT * FROM PRODUCT WHERE PID = ?"
        prostmt = ibm_db.prepare(conn,productsql)
        ibm_db.bind_param(prostmt,1,proid)
        ibm_db.execute(prostmt)
        product = ibm_db.fetch_assoc(prostmt)
        productname = product['PNAME']
        o['NAME'] = productname 
        farid = o['FID']
        farmsql = "SELECT * FROM FARMERS WHERE FID = ?"
        farmstmt = ibm_db.prepare(conn,farmsql)
        ibm_db.bind_param(farmstmt,1,farid)
        ibm_db.execute(farmstmt)
        farm = ibm_db.fetch_assoc(farmstmt)
        o['FNAME'] = farm['FNAME']
        o['FPH'] = farm['FPHONE']
        orders.append(o)
        o = ibm_db.fetch_assoc(orstmt)
    
    hsql="SELECT * FROM ORDER WHERE HID = ? AND NOT (STATUS = 'Yet to deliver' OR STATUS = 'Confirmed by Farmer') ORDER BY TIME DESC"
    hstmt = ibm_db.prepare(conn,hsql)
    ibm_db.bind_param(hstmt,1,hid)
    ibm_db.execute(hstmt)
    h = ibm_db.fetch_assoc(hstmt)
    orderh = []
    while h:
        proid = h['PID']
        productsql = "SELECT * FROM PRODUCT WHERE PID = ?"
        prostmt = ibm_db.prepare(conn,productsql)
        ibm_db.bind_param(prostmt,1,proid)
        ibm_db.execute(prostmt)
        product = ibm_db.fetch_assoc(prostmt)
        productname = product['PNAME']
        h['NAME'] = productname 
        farid = h['FID']
        farmsql = "SELECT * FROM FARMERS WHERE FID = ?"
        farmstmt = ibm_db.prepare(conn,farmsql)
        ibm_db.bind_param(farmstmt,1,farid)
        ibm_db.execute(farmstmt)
        farm = ibm_db.fetch_assoc(farmstmt)
        h['FNAME'] = farm['FNAME']
        h['FPH'] = farm['FPHONE']
        orderh.append(h)
        h = ibm_db.fetch_assoc(hstmt)
    return render_template('horder.html',order = orders,orderh=orderh)

@app.route('/corder/<oid>')
def corder(oid):
    qsql = "SELECT * FROM  ORDER WHERE OID = ?"
    qstmt = ibm_db.prepare(conn,qsql)
    ibm_db.bind_param(qstmt,1,oid)
    ibm_db.execute(qstmt)
    orderq = ibm_db.fetch_assoc(qstmt)
    oq = orderq['OQUANTITY']
    pid =orderq['PID']
    stat =orderq['STATUS']
    
    psql = "SELECT * FROM PRODUCT WHERE PID = ?"
    pstmt = ibm_db.prepare(conn,psql)
    ibm_db.bind_param(pstmt,1,pid)
    ibm_db.execute(pstmt)
    productq = ibm_db.fetch_assoc(pstmt)
    pq = productq['PQUANTITY']
    npq = float(pq) + float(oq) 

    upq = "UPDATE PRODUCT SET PQUANTITY = ? WHERE PID = ?"
    upstmt = ibm_db.prepare(conn,upq)
    ibm_db.bind_param(upstmt,1,npq)
    ibm_db.bind_param(upstmt,2,pid)
    ibm_db.execute(upstmt)

    csql = "UPDATE ORDER SET STATUS = 'Canceled' WHERE OID = ?"
    cstmt = ibm_db.prepare(conn,csql)
    ibm_db.bind_param(cstmt,1,oid)
    ibm_db.execute(cstmt)
    hid = session['hid']

    orsql="SELECT * FROM ORDER WHERE HID = ? AND NOT STATUS = 'Canceled'"
    orstmt = ibm_db.prepare(conn,orsql)
    ibm_db.bind_param(orstmt,1,hid)
    ibm_db.execute(orstmt)
    o = ibm_db.fetch_assoc(orstmt)
    orders = []
    while o:
        proid = o['PID']
        productsql = "SELECT * FROM PRODUCT WHERE PID = ?"
        prostmt = ibm_db.prepare(conn,productsql)
        ibm_db.bind_param(prostmt,1,proid)
        ibm_db.execute(prostmt)
        product = ibm_db.fetch_assoc(prostmt)
        productname = product['PNAME']
        o['NAME'] = productname 
        farid = o['FID']
        
        farmsql = "SELECT * FROM FARMERS WHERE FID = ?"
        farmstmt = ibm_db.prepare(conn,farmsql)
        ibm_db.bind_param(farmstmt,1,farid)
        ibm_db.execute(farmstmt)
        farm = ibm_db.fetch_assoc(farmstmt)
        o['FNAME'] = farm['FNAME']
        o['FPH'] = farm['FPHONE']
        orders.append(o)
        o = ibm_db.fetch_assoc(orstmt)
    
    hsql="SELECT * FROM ORDER WHERE HID = ? AND NOT (STATUS = 'Yet to deliver' OR STATUS = 'Confirmed by Farmer') ORDER BY TIME DESC"
    hstmt = ibm_db.prepare(conn,hsql)
    ibm_db.bind_param(hstmt,1,hid)
    ibm_db.execute(hstmt)
    h = ibm_db.fetch_assoc(hstmt)
    orderh = []
    while h:
        proid = h['PID']
        productsql = "SELECT * FROM PRODUCT WHERE PID = ?"
        prostmt = ibm_db.prepare(conn,productsql)
        ibm_db.bind_param(prostmt,1,proid)
        ibm_db.execute(prostmt)
        product = ibm_db.fetch_assoc(prostmt)
        productname = product['PNAME']
        h['NAME'] = productname 
        farid = h['FID']
        farmsql = "SELECT * FROM FARMERS WHERE FID = ?"
        farmstmt = ibm_db.prepare(conn,farmsql)
        ibm_db.bind_param(farmstmt,1,farid)
        ibm_db.execute(farmstmt)
        farm = ibm_db.fetch_assoc(farmstmt)
        h['FNAME'] = farm['FNAME']
        h['FPH'] = farm['FPHONE']
        orderh.append(h)
        h = ibm_db.fetch_assoc(hstmt)
    return render_template('horder.html',order = orders,orderh=orderh)

@app.route('/tfee')
def tfee():
    return render_template('fees.html')

@app.route('/forder')
def forder():
    fid = session['fid']
    fosql = "SELECT * FROM ORDER WHERE FID = ? AND (STATUS = 'Yet to deliver' OR STATUS = 'Confirmed by Farmer')"
    fostmt = ibm_db.prepare(conn,fosql)
    ibm_db.bind_param(fostmt,1,fid)
    ibm_db.execute(fostmt)
    order = ibm_db.fetch_assoc(fostmt)
    forders = []
    while order:
        hid = order['HID']
        pid = order['PID']
        psql  = "SELECT * FROM PRODUCT WHERE PID = ?"
        pstmt = ibm_db.prepare(conn,psql)
        ibm_db.bind_param(pstmt,1,pid)
        ibm_db.execute(pstmt)
        pro = ibm_db.fetch_assoc(pstmt)
        order['NAME'] = pro['PNAME']
        hsql = "SELECT * FROM HOSTEL WHERE HID = ?"
        hstmt = ibm_db.prepare(conn,hsql)
        ibm_db.bind_param(hstmt,1,hid)
        ibm_db.execute(hstmt)
        hostel = ibm_db.fetch_assoc(hstmt)
        order['HNAME'] = hostel['HNAME']
        order['HPH'] = hostel['HPHONE']
        order['HADD'] = hostel['HADDRESS']
        forders.append(order)
        order = ibm_db.fetch_assoc(fostmt)
    
    fhsql = "SELECT * FROM ORDER WHERE FID = ? AND NOT (STATUS = 'Yet to deliver' OR STATUS = 'Confirmed by Farmer') ORDER BY TIME DESC"
    fhstmt = ibm_db.prepare(conn,fhsql)
    ibm_db.bind_param(fhstmt,1,fid)
    ibm_db.execute(fhstmt)
    horder = ibm_db.fetch_assoc(fhstmt)
    fhorders = []
    while horder:
        hid = horder['HID']
        pid = horder['PID']
        psql  = "SELECT * FROM PRODUCT WHERE PID = ?"
        pstmt = ibm_db.prepare(conn,psql)
        ibm_db.bind_param(pstmt,1,pid)
        ibm_db.execute(pstmt)
        pro = ibm_db.fetch_assoc(pstmt)
        horder['NAME'] = pro['PNAME']
        hsql = "SELECT * FROM HOSTEL WHERE HID = ?"
        hstmt = ibm_db.prepare(conn,hsql)
        ibm_db.bind_param(hstmt,1,hid)
        ibm_db.execute(hstmt)
        hostel = ibm_db.fetch_assoc(hstmt)
        horder['HNAME'] = hostel['HNAME']
        horder['HPH'] = hostel['HPHONE']
        horder['HADD'] = hostel['HADDRESS']
        fhorders.append(horder)
        horder = ibm_db.fetch_assoc(fostmt)
    return render_template('forders.html',order = forders,orderh=fhorders)

@app.route('/confirmorder/<oid>')
def confirmorder(oid):
    consql = "UPDATE ORDER SET STATUS = 'Confirmed by Farmer' WHERE OID = ?"
    constmt = ibm_db.prepare(conn,consql)
    ibm_db.bind_param(constmt,1,oid)
    ibm_db.execute(constmt)
    fid = session['fid']
    fosql = "SELECT * FROM ORDER WHERE FID = ? AND (STATUS = 'Yet to deliver' OR STATUS = 'Confirmed by Farmer')"
    fostmt = ibm_db.prepare(conn,fosql)
    ibm_db.bind_param(fostmt,1,fid)
    ibm_db.execute(fostmt)
    order = ibm_db.fetch_assoc(fostmt)
    forders = []
    while order:
        hid = order['HID']
        pid = order['PID']
        psql  = "SELECT * FROM PRODUCT WHERE PID = ?"
        pstmt = ibm_db.prepare(conn,psql)
        ibm_db.bind_param(pstmt,1,pid)
        ibm_db.execute(pstmt)
        pro = ibm_db.fetch_assoc(pstmt)
        order['NAME'] = pro['PNAME']
        hsql = "SELECT * FROM HOSTEL WHERE HID = ?"
        hstmt = ibm_db.prepare(conn,hsql)
        ibm_db.bind_param(hstmt,1,hid)
        ibm_db.execute(hstmt)
        hostel = ibm_db.fetch_assoc(hstmt)
        order['HNAME'] = hostel['HNAME']
        order['HPH'] = hostel['HPHONE']
        order['HADD'] = hostel['HADDRESS']
        forders.append(order)
        order = ibm_db.fetch_assoc(fostmt)
    
    fhsql = "SELECT * FROM ORDER WHERE FID = ? AND NOT (STATUS = 'Yet to deliver' OR STATUS = 'Confirmed by Farmer') ORDER BY TIME DESC"
    fhstmt = ibm_db.prepare(conn,fhsql)
    ibm_db.bind_param(fhstmt,1,fid)
    ibm_db.execute(fhstmt)
    horder = ibm_db.fetch_assoc(fhstmt)
    fhorders = []
    while horder:
        hid = horder['HID']
        pid = horder['PID']
        psql  = "SELECT * FROM PRODUCT WHERE PID = ?"
        pstmt = ibm_db.prepare(conn,psql)
        ibm_db.bind_param(pstmt,1,pid)
        ibm_db.execute(pstmt)
        pro = ibm_db.fetch_assoc(pstmt)
        horder['NAME'] = pro['PNAME']
        hsql = "SELECT * FROM HOSTEL WHERE HID = ?"
        hstmt = ibm_db.prepare(conn,hsql)
        ibm_db.bind_param(hstmt,1,hid)
        ibm_db.execute(hstmt)
        hostel = ibm_db.fetch_assoc(hstmt)
        horder['HNAME'] = hostel['HNAME']
        horder['HPH'] = hostel['HPHONE']
        horder['HADD'] = hostel['HADDRESS']
        fhorders.append(horder)
        horder = ibm_db.fetch_assoc(fostmt)
    return render_template('forders.html',order = forders,orderh=fhorders)

@app.route('/hdelivered/<oid>')
def hdelivered(oid):
    return render_template('rating.html',oid=oid)

@app.route('/rate')
def rate():
    rating = int(request.args.get('rating'))
    oid = request.args.get('oid')
    osql = "SELECT * FROM ORDER WHERE OID = ?"
    ostmt = ibm_db.prepare(conn,osql)
    ibm_db.bind_param(ostmt,1,oid)
    ibm_db.execute(ostmt)
    order = ibm_db.fetch_assoc(ostmt)
    pid = order['PID']

    psql = "SELECT * FROM PRODUCT WHERE PID = ?"
    pstmt = ibm_db.prepare(conn,psql)
    ibm_db.bind_param(pstmt,1,pid)
    ibm_db.execute(pstmt)
    product = ibm_db.fetch_assoc(pstmt)
    exrate = int(product['RATING'])
    norate = int(product['NORATE'])
    if exrate == 0 and norate == 0:
        norate = 1
        rate = rating
    else:
        rate = (exrate + rating) / 2
        norate = norate + 1

    rate = round(rate)
    rsql = "UPDATE PRODUCT SET RATING = ? , NORATE = ? WHERE PID = ?"
    rstmt = ibm_db.prepare(conn,rsql)
    ibm_db.bind_param(rstmt,1,rate)
    ibm_db.bind_param(rstmt,2,norate)
    ibm_db.bind_param(rstmt,3,pid)
    ibm_db.execute(rstmt)

    sql = "UPDATE ORDER SET STATUS = 'Delivered' WHERE OID = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,oid)
    ibm_db.execute(stmt)
    return render_template('hhome.html')
































@app.route('/flogout')
def flogout():
    session['loggedin']=False
    session.pop('fid',None)
    session.pop('fname',None)
    session.pop('floc',None)
    return render_template('login.html')


@app.route('/hlogout')
def hlogout():
    session['loggedin']=False
    session.pop('hid',None)
    session.pop('hname',None)
    session.pop('hloc',None)
    return render_template('login.html')


if __name__ == '__main__':
    app.debug == True
    app.run(host='0.0.0.0')