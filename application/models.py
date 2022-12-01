from application import db

# create crypto table 
class Crypto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Bmi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float(), nullable=False) # centimetres
    weight = db.Column(db.Float(), nullable=False) # pounds
    bmi_result = db.Column(db.Float(),nullable=True) #bmi points

# create database
db.create_all()