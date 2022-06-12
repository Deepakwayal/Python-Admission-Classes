from flask import *
import pymysql

db = pymysql.connect(
    host="localhost",
    user ="root",
    password="",
    database="danceinfo"
    
    )
cursor =db.cursor()


app =Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dance")
def dance():
    return render_template("dance.html")

@app.route("/classes")
def classes():
    cursor.execute("select * from student")
    data =cursor.fetchall()
    return render_template("classes.html",userdata=data)

@app.route("/user/<name>")
def user(name):
    return "Hello {}".format(name)


@app.route("/create",methods=["POST"])
def create():
    fname=request.form.get('firstname')
    lname=request.form.get('lastname')
    contact=request.form.get('contact')
    gender=request.form.get('gender')
    city=request.form.get('city')
    dancestyle=request.form.get('dancestyle')
    insq="insert into student(First_Name,Last_Name,Contact_Number,Gender,City,Dance_Style) values ('{}','{}','{}','{}','{}','{}')".format(fname,lname,contact,gender,city,dancestyle)
    try:
        cursor.execute(insq)
        db.commit()
        return redirect(url_for('classes'))
    except:
        db.rollback()
        return "Error in query"
    
@app.route("/delete")
def delete():
    id=request.args.get('id')
    delq="delete from student where id={}".format(id)
    try:
        cursor.execute(delq)
        db.commit()
        return redirect(url_for("classes"))
    except:
        db.rollback()
        return "Error in query"   

@app.route("/edit")
def edit():
    id=request.args.get('id')
    selq="select * from student where id={}".format(id)
    cursor.execute(selq)
    data=cursor.fetchone()
    return render_template("edit.html",row=data)    

@app.route("/update",methods=["POST"])
def update():
    fname=request.form.get('firstname')
    lname=request.form.get('lastname')
    contact=request.form.get('contact')
    gender=request.form.get('gender')
    city=request.form.get('city')
    dancestyle=request.form.get('dancestyle')
    uid=request.form.get('uid')
    
    insq="update student set First_Name='{}',Last_Name='{}',Contact_Number='{}',Gender='{}',City='{}',Dance_Style='{}' where id='{}' ".format(fname,lname,contact,gender,city,dancestyle,uid)
    try:
        cursor.execute(insq)
        db.commit()
        return redirect(url_for('classes'))
    except:
        db.rollback()
        return "Error in query"



@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/getdata",methods=["POST"])
def getdata():
    id=request.form.get('id')
    selq="select * from student where id={}".format(id)
    
    cursor.execute(selq)
    data=cursor.fetchone()
    return render_template("search.html",row=data) 

if __name__=="__main__":
    app.run(debug=True)