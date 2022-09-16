from flask import Flask,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:root@localhost/Employee_Details"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
app.config["SQLALCHEMY_ECHO"]=True

db=SQLAlchemy(app)
actors_association=db.Table("actors_association",db.Column("actors_id",
                    db.Integer(),db.ForeignKey("actors.Id")),
                    db.Column("address_id",db.Integer(),db.ForeignKey("actors_address.id")))

class actors(db.Model):#one to one relationship
    __tablename__="actors"
    id=db.Column("Id",db.Integer(),primary_key=True)
    name = db.Column("Name", db.String(100), nullable=False)
    year = db.Column("year", db.String(100), nullable=False)

    adhar_actor=db.relationship("actors_adhar",backref="actors",lazy=True,uselist=False,cascade="all,delete")
    address_actor = db.relationship("actors_address",secondary=actors_association, backref="actors", lazy="joined",cascade="all,delete")


    def __repr__(self):
        if self.adhar_actor:
            adhar_actor=self.adhar_actor.__repr__()
        else:
            adhar_actor={}
        return {"id":self.id,"name":self.name,"year":self.year,"adhar_actor":adhar_actor}

class actors_adhar(db.Model):#class actors_adhar(db.Model)
    __tablename__="actors_adhar"
    id=db.Column("id",db.Integer(),primary_key=True)
    adhar = db.Column("adhar", db.Integer(), nullable=False)
    actors_id = db.Column("actors_id", db.Integer(), db.ForeignKey("actors.Id"),nullable=False)
    def __repr__(self):
        return {"adhar":self.adhar}

class actors_address(db.Model):#class actors_adhar(db.Model)
    __tablename__="actors_address"
    id=db.Column("id",db.Integer(),primary_key=True)
    address = db.Column("address", db.String(250), nullable=False)

    def __repr__(self):
        return {"address":self.address}

@app.route("/POST",methods=["POST"])
def POST():
    id=request.form.get("id")
    name = request.form.get("name")
    year = request.form.get("year")
    user_details=actors(id=id,name=name,year=year)
    db.session.add(user_details)
    db.session.commit()
    return "user added"

@app.route("/GET",methods=["GET"])
def GET():
    user_details=actors.query.all()
    user=[x.__repr__() for x in user_details]
    return user

@app.route("/POST1",methods=["POST"])
def POST_adhar():
    id=request.form.get("id")
    adhar = request.form.get("adhar")
    actors_id = request.form.get("actors_id")
    user_details=actors_adhar(id=id,adhar=adhar,actors_id=actors_id)
    db.session.add(user_details)
    db.session.commit()
    return "adhar added"

@app.route("/POST_address",methods=["POST"])
def POST_address():
    id=request.form.get("id")
    address = request.form.get("address")
    user_details=actors_address(id=id,address=address)
    data=actors.query.get(id)
    data.address_actor.append(user_details)
    db.session.add(user_details)
    db.session.commit()
    return "user_address added"


if __name__=="__main__":
    db.create_all()
    app.run(debug=True,port=7000)