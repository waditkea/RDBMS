from flask import Flask,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:root@localhost/Employee_Details"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
app.config["SQLALCHEMY_ECHO"]=True

db=SQLAlchemy(app)

@app.route("/CREAT", methods=["GET"])
def CREAT():
    return "hello world"

class Engineer(db.Model):
    __tablename__="Engineer1"
    id=db.Column("Id",db.Integer(),primary_key=True)
    name = db.Column("Name", db.String(100), nullable=False)
    address = db.Column("Address", db.String(200), nullable=False)
    year = db.Column("year", db.String(100), nullable=False)

    def __repr__(self):
        return {"id":self.id,"name":self.name,"address":self.address,"year":self.year}

@app.route("/GET", methods=["GET"])
def GET():
    user_details=Engineer.query.all()
    user=[x.__repr__() for x in user_details]
    if user==[]:
        return "data not found"
    else:
        return user

@app.route("/GET1/<int:id>", methods=["GET"])
def GET1(id):
    user_details=Engineer.query.get(id)
    user=user_details.__repr__()
    if user==[]:
        return "data not found"
    else:
        return user

@app.route("/GET2", methods=["GET"])
def GET2():
    user_details=request.args.get("name")
    user=Engineer.query.filter(Engineer.name==user_details).first()
    user_1=user.__repr__()
    return user_1

@app.route("/GET3/<name>", methods=["GET"])
def GET3(name):
    user_details=Engineer.query.all()
    user_1 = [x.__repr__() for x in user_details]
    user=[x for x in user_1 if x["name"]==name]
    return user

@app.route("/GET4/<year>", methods=["GET"])
def GET4(year):
    user_details=Engineer.query.filter(Engineer.year==year)
    user_1 = [x.__repr__() for x in user_details]
    return user_1


@app.route("/POST", methods=["POST"])
def POST():
    id=request.form.get("id")
    name = request.form.get("name")
    address = request.form.get("address")
    user_details=Engineer(id=id,name=name,address=address)
    db.session.add(user_details)
    db.session.commit()
    return "user added"

@app.route("/POST1", methods=["POST"])
def POST1():
    user=request.get_json()
    id=user["id"]
    name = user["name"]
    address = user["address"]
    user_details=Engineer(id=id,name=name,address=address)
    db.session.add(user_details)
    db.session.commit()
    return "user added"

@app.route("/POST2", methods=["GET","POST"])#get and post method through same end point
def POST2():
    if request.method=="POST":
        user=request.get_json()
        id=user["id"]
        name = user["name"]
        address = user["address"]
        user_details=Engineer(id=id,name=name,address=address)
        db.session.add(user_details)
        db.session.commit()
        return "user added"
    if request.method == "GET":
        user_details=Engineer.query.all()
        user=[x.__repr__( ) for x in user_details]
        return user


@app.route("/PUT/<int:id>", methods=["PUT"])
def PUT(id):
    user_details=Engineer.query.get(id)
    name=request.form.get("name")
    address = request.form.get("address")
    user_details.name=name
    user_details.address = address
    db.session.commit()
    return "user updated"

@app.route("/PUT1", methods=["PUT"])
def PUT1():
    user_details=request.get_json()
    id=user_details["id"]
    name = user_details["name"]
    address = user_details["address"]
    user=Engineer.query.get(id)
    user.name=name
    user.address = address
    db.session.commit()
    return "user updated"

@app.route("/PUT2", methods=["PUT"])
def PUT2():
    user_details=request.args.get("name")
    user=Engineer.query.filter(Engineer.name==user_details).first()
    address=request.form.get("address")
    user.address=address
    db.session.commit()
    return "user updated"

@app.route("/PUT3", methods=["PUT"])
def PUT3():
    name=request.form.get("name")
    address = request.form.get("address")
    user=Engineer.query.filter(Engineer.name==name).update(dict(address=address))
    db.session.commit()
    return "user updated"

@app.route("/PUT4/<name>", methods=["PUT"])
def PUT4(name):
    user = Engineer.query.filter(Engineer.name == name).first()
    address = request.form.get("address")
    user.address=address
    db.session.commit()
    return "user updated"


@app.route("/DELETE/<int:id>", methods=["DELETE"])
def DELETE(id):
    user_details=Engineer.query.get(id)
    db.session.delete(user_details)
    db.session.commit()
    return "user deleted"

@app.route("/DELETE1", methods=["DELETE"])
def DELETE1():
    year=request.form.get("year")
    Engineer.query.filter(Engineer.year==year).delete()
    db.session.commit()
    return "user deleted"

if __name__=="__main__":
    db.create_all()
    app.run(debug=True,port=3000)

