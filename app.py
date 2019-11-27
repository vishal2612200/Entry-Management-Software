from flask import Flask,render_template,flash, redirect,url_for,session,request
from flask_sqlalchemy import SQLAlchemy
import smtplib,time
import urllib.request
import urllib.parse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)



class host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    husername = db.Column(db.String(80))
    hemail = db.Column(db.String(120))
    userphone = db.Column(db.String(80))

class visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    visitorphone = db.Column(db.String(120))
    checkin = db.Column(db.String(120))


def host_send_email(m,n,o,p,q):
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com',587) 
    # start TLS for security 
    s.starttls() 
    # Authentication 
    s.login("innovaccersummergeeks@gmail.com", "testing@123") 
    

    # message to be sent 
    text = "Hi Host,\n Visitor Name:\t"+ m +"\n Visitor Email:\t"+ n +"\n Visitor Phone\t"+ o+"\n Checkin Time:\t"+ p+"IST"+"\n visitor had just check in"
    subject = "Visitor has just checked in"
    message = 'Subject: {}\n\n{}'.format(subject, text)
    # sending the mail 
    s.sendmail("innovaccersummergeeks@gmail.com", q, message) 
        
    # terminating the session 
    s.quit()     



def visitor_send_email(a,b,c,d,e,f):
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com',587) 
    # start TLS for security 
    s.starttls() 
    # Authentication 
    s.login("innovaccersummergeeks@gmail.com", "testing@123") 
    
    #t = time.localtime()
    #current_time = time.strftime("%H:%M:%S", t)   
    # message to be sent 
    text = "Thank you Visitor for visiting us,\n Visitor Name:\t"+ a +"\n Visitor Phone:\t"+ c +"\n Check-in Time:\t"+ d+"IST"+"\n Check-out Time:\t"+ e +"\n Host Name:\t"+ f + "\n Address visited : Summergeeks by innovaccer" 
    subject = "Visitor has just checked in"
    message = 'Subject: {}\n\n{}'.format(subject, text)
    # sending the mail 
    s.sendmail("innovaccersummergeeks@gmail.com", b, message) 
        
    # terminating the session 
    s.quit()     



 
def sendSMS(apikey, numbers, sender, message):
    data = urllib.parse.urlencode({'apikey': '3LVJW9iNFVc-EaMh9LZLGuogPU33ec2HNPB3cr7oDV', 'numbers': numbers,'message':message,'sender':'TXTLCL'})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)
 
#resp =  sendSMS('apikey', '919149189644','Jims Autos', 'This is your message')







@app.route("/")
def index():
    return render_template("index.html")



@app.route("/hostverify",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = host.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/host", methods=["GET", "POST"])
def hostpage():
    if request.method == "POST":
        hname = request.form['name']
        hemail = request.form['email']
        hphonenumber = request.form['phonenumber']

        hregister = host(husername = hname, hemail = hemail, userphone = hphonenumber)
        db.session.add(hregister)
        db.session.commit()

        return redirect(url_for("hostthank"))
    return render_template("host.html")
@app.route("/hostthank", methods=["GET", "POST"])
def hostthank():
    return render_template("hostthank.html")
@app.route("/hostcheck")
def hostcheck():


        
    hrecords = host.query.order_by(host.id.desc()).first()
        
    host_email = hrecords.__dict__['hemail']  
    host_phone = hrecords.__dict__['userphone']         
    vrecord = visitor.query.order_by(visitor.id.desc()).first()
    visitor_names = vrecord.__dict__['username']
    visitor_emails = vrecord.__dict__['email']
    visitor_phones = vrecord.__dict__['visitorphone']
    visitor_checkins= vrecord.__dict__['checkin']
    host_send_email(visitor_names,visitor_emails,visitor_phones,visitor_checkins,host_email)
    sms_mes = "Name:\t" +  visitor_names + "\nEmail:\t" + visitor_emails + "\nPhone:\t" + visitor_phones + "\nCheckin:\t" + visitor_checkins
    sendSMS('apikey', host_phone ,'Innovaccer', sms_mes)
        
    return render_template("hostcheck.html")
@app.route("/visitoremail" , methods=["GET", "POST"])
def visitoremail():
    if request.method == "POST":
        
        vrecords = visitor.query.order_by(visitor.id.desc()).first()
        
        visitor_name = vrecords.__dict__['username']
        visitor_email = vrecords.__dict__['email']
        visitor_phone = vrecords.__dict__['visitorphone']
        visitor_checkin = vrecords.__dict__['checkin']
        vt = time.localtime()
        visitor_checkout = time.strftime("%H:%M:%S", vt) 
        hrecord = host.query.order_by(host.id.desc()).first()
        hostnames = hrecord.__dict__['husername']
        #print(hrecord)
        visitor_send_email(visitor_name,visitor_email,visitor_phone,visitor_checkin,visitor_checkout,hostnames)
        return render_template("thankvisitor.html")

@app.route("/visitorinfo", methods=["GET", "POST"])
def visitorinfo():
    if request.method == "POST":
        firstname = request.form['first-name']
        lastname = request.form['last-name']
        vname = firstname+" " +lastname
        visemail = request.form['vemail']
        visphone = request.form['vphone']
        vist = time.localtime()
        visitor_checkin = time.strftime("%H:%M:%S", vist)
        

        vregister = visitor(username = vname, email = visemail, visitorphone = visphone, checkin = visitor_checkin)
        db.session.add(vregister)
        db.session.commit()

        return redirect(url_for("hostcheck"))
    return render_template("visitor.html")    


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = host(username = uname, email = mail, userphone = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
