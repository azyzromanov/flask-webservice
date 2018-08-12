from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import PrimaryKeyConstraint
from flask import Flask,jsonify
from datetime import datetime


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


# Define the Category DataModel
class Category(db.Model):
	__tablename__ = 'category'
	id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
	label = db.Column(db.String(50), unique=True)

	def __init__(self,label):
		self.label = label


	def toJSON(self):
		return {'id':self.id,'label': self.label}


	def exists(label):
		res = Category.query.filter_by(label=label).first()
		if (res):
			return True
		return False


	def search_by_label(label):
		res = Category.query.filter_by(label=label).first()
		if (res):
			return res
		return False

	def search_by_id(id):
		res = Category.query.filter_by(id=id).first()
		if (res):
			return res
		return False


# Define the Product DataModel
class Product(db.Model):
	__tablename__ = 'product'

	id = db.Column(db.Integer(), primary_key=True)
	label = db.Column(db.String(50), unique=True)
	category_id = db.Column(db.Integer(), db.ForeignKey('category.id'))
	create_date = db.Column(db.Date(),default=datetime.utcnow)
	category = db.relationship("Category", foreign_keys=[category_id])

	def __init__(self,label,category_id):
		self.label = label
		self.category_id = category_id

	def exists(label):
		res = Product.query.filter_by(label=label).first()
		if (res):
			return True
		return False

	def search_by_label(label):
		res = Product.query.filter_by(label=label).first()
		if (res):
			return res
		return False

	def search_by_id(id):
		res = Product.query.filter_by(id=id).first()
		if (res):
			return res
		return False

	def search_by_category(id):
		res = Product.query.filter_by(category_id=category_id)
		if (res):
			return res
		return False

	def toJSON(self):
		return {'id':self.id,'label':self.label,'category_id': self.category.toJSON()}