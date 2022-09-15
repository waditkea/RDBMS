from flask import Flask,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:root@localhost/Employee_Details"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
app.config["SQLALCHEMY_ECHO"]=True

db=SQLAlchemy(app)

class politicians(db.Model):
    __tablename__="politicians"
    id=db.Column("Id",db.Integer(),primary_key=True)
    name = db.Column("Name", db.String(100), nullable=False)
    address = db.Column("Address", db.String(200), nullable=False)
    year = db.Column("year", db.String(100), nullable=False)

    def __repr__(self):
        return {"id":self.id,"name":self.name,"address":self.address,"year":self.year}


@app.route("/GET",methods=["GET"])
def GET():
    if request.method=="GET":
        user_details=politicians.query.all()
        return render_template("index.html",user_details=user_details)

@app.route("/POST",methods=["GET","POST"])
def POST():
    if request.method=="GET":
        return render_template("post.html")
    if request.method=="POST":
        id=request.form.get("Id")
        name = request.form.get("Name")
        address = request.form.get("Address")
        year = request.form.get("Year")
        user_details=politicians(id=id,name=name,address=address,year=year)
        db.session.add(user_details)
        db.session.commit()
        return redirect("/GET")

@app.route("/delete/<int:id>")
def DELETE(id):
        user_details=politicians.query.get(id)
        db.session.delete(user_details)
        db.session.commit()
        return redirect("/GET")

@app.route("/PUT/<int:id>")
def PUT(id):
        user_details=politicians.query.get(id)
        return render_template("PUT.html",user_details=user_details)

@app.route("/PUT1", methods=["POST"])
def PUT1():
    id = request.form.get("Id")
    name = request.form.get("Name")
    address=request.form.get("Address")
    year = request.form.get("Year")
    user_details = politicians.query.get(id)
    user_details.name=name
    user_details.address = address
    user_details.year = year
    db.session.commit()
    return redirect("/GET")







if __name__=="__main__":
    db.create_all()
    app.run(debug=True,port=7000)