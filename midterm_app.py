# Add to this file for the sample app lab
from flask import Flask, url_for, redirect, jsonify, request
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json, os
import sqlite3 as sql
from datetime import datetime


webApp = Flask(__name__)
webApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Customer.sqlite'
webApp.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
db = SQLAlchemy(webApp)
ma = Marshmallow(webApp)

class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.String(50), primary_key=True)
    customer_fname = db.Column(db.String(50))
    customer_lname = db.Column(db.String(50))
    customer_uname = db.Column(db.String(50))
    customer_password = db.Column(db.String(50))

    def __init__(self, customer_id, customer_fname, customer_lname,customer_uname, customer_password):
        self.customer_id = customer_id
        self.customer_fname = customer_fname
        self.customer_lname = customer_lname
        self.customer_uname = customer_uname
        self.customer_password = customer_password
        

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ("customer_id", "customer_fname" , "customer_lname","customer_uname", "customer_password")

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


@webApp.route("/")
def main():
    return render_template("login.html")



@webApp.route('/register')
def register():
    # show the form, it wasn't submitted
    return render_template('registration.html')

@webApp.route('/createdAcc', methods=['GET', 'POST'])
def createdAcc():
    if request.method == 'POST':
        customer_id = datetime.now().strftime("%Y%m%d%H%M%S")
        customer_fname = request.form["fname_signup"]
        customer_lname = request.form["lname_signup"]
        customer_uname = request.form['uname_signup']
        customer_password = request.form['password_signup']
        new_customer = Customer(customer_id, customer_fname,customer_lname, customer_uname, customer_password)
        db.session.add(new_customer)
        db.session.commit()
        customer_schema.jsonify(new_customer)
        
        return render_template('login.html')


if __name__ == "__main__":
    webApp.run(host="0.0.0.0", port=5000, debug=True)
