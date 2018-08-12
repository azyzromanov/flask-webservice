from flask import Flask,request,jsonify,make_response,abort,Response
from . import app
from .models import Category,Product,db
from flask_sqlalchemy import SQLAlchemy

import json


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
	message = {
			'status': 404,
			'message': 'Not found',
	}
	return jsonify(message)


@app.route('/')
def index():
	message = {
			'status': 1,
			'message': 'It works...',
	}
	return jsonify(message)

# Add category
@app.route('/category/add' , methods = ['POST'])
def addCategory():
	try:
		if request.method == 'POST':
			data = request.form
			category = Category(label=data['label'])

			# we check if the category with the same label exists
			if (Category.search_by_label(data['label'])):

				message = {
					'status': 1,
					'message': 'This category already exists !',
					'data' : None
				}

				return jsonify(message)

			db.session.add(category)
			db.session.commit()
			message = {
					'status': 1,
					'message': 'Category has been successfully created !',
					'data' : category.toJSON()
			}

			return jsonify(message)

	except:

		message = {
				'status': -1,
				'message': 'Error !',
				'data' : None
		}
		return jsonify(message)


			
# Edit category
@app.route('/category/edit/<id>' , methods = ['POST'])
def editCategory(id):

	try:

		category = db.session.query(Category).get(id)
		data = request.form
		if category:

			category.label = data['label']
			db.session.add(category)
			db.session.commit()

			message = {
					'status': 1,
					'message': 'Category has been successfully updated !',
					'data' : category.toJSON()
			}

		else:

			message = {

					'status': 0,
					'message': 'This category does not exists!',
					'data' : None
			}

	except:

		message = {
				'status': -1,
				'message': 'Error !',
				'data' : None
		}

	return jsonify(message)

# delete category
@app.route('/category/delete/<id>/<method>' , methods = ['GET'])
def deleteCategory(id,method):

	try:
		category = db.session.query(Category).get(id)

		if category:

			if method.lower() == "cascade":

				products = Product.query.filter_by(category_id=id)
				
				for product in products:
					deleteProduct(product.id)


				message = {
					'status': 1,
					'message': 'Category has been successfully deleted and all the linked products as well !',
					'data' : None
				}

			else:

				message = {
						'status': 1,
						'message': 'Category has been successfully deleted !',
						'data' : None
				}


			db.session.delete(category)
			db.session.commit()

		else:
			message = {
						'status': 0,
						'message': 'This category does not exists !',
						'data' : None
				}

	except:

		message = {

			'status': -1,
			'message': 'Error !',
			'data' : None
		}

	return jsonify(message)

# List category
@app.route('/category/list' , methods = ['GET'])
def listCategory():
	try:
		categories = Category.query.all()
		data = []

		for cat in categories:
			data.append(cat.toJSON())

		message = {
					'status': 1,
					'message': 'Categories list !',
					'data' : data
			}
	except:
		message = {
			'status': - 1,
			'message': 'Error !',
			'data' : None
		}

	return jsonify(message)


# Add product
@app.route('/product/add' , methods = ['POST'])
def addProduct():
	try:
		if request.method == 'POST':
			data = request.form

			if ((Product.exists(data['label']))):
				message = {
					'status': 0,
					'message': 'This product already exists  !',
					'data' : None
				}

			if Category.search_by_id(data['category_id']):
				product = Product(label=data['label'] , category_id =data['category_id'])
				db.session.add(product)
				db.session.commit()

				message = {
					'status': 1,
					'message': 'Product has been successfully created !',
					'data' : product.toJSON()
				}

			else:

				message = {
					'status': 0,
					'message': 'The specified category does not exist!',
					'data' : None
				}

	except:
		message = {
			'status': -1,
			'message': 'Error !',
			'data' : None
		}
	
	return jsonify(message)
			
# Edit product
@app.route('/product/edit/<id>' , methods = ['GET','POST'])
def editProduct(id):

	try:
		product = db.session.query(Product).get(id)

		if request.method == 'POST':
			data = request.form

			if 'label' not in data or 'category_id' not in data:

				message = {
						'status': 1,
						'message': 'Label and category_id are mandatories fields !',
						'data' : None
					}


			if Category.search_by_id(data['category_id']):

				product.label = data['label']
				product.category_id = data['category_id']
				db.session.add(product)
				db.session.commit()

				message = {
						'status': 1,
						'message': 'Product has been successfully created !',
						'data' : product.toJSON()
					}

			else:

				message = {
						'status': 0,
						'message': 'The specified category does not exist !',
						'data' : None
					}

	except:

		message = {
			'status': - 1,
			'message': 'Error !',
			'data' : None
		}
	
	return jsonify(message)

# Delete product
@app.route('/product/delete/<id>' , methods = ['GET'])
def deleteProduct(id):
	try:

		product = db.session.query(Product).get(id)

		if product:

			db.session.delete(product)
			db.session.commit()
			message = {
						'status': 1,
						'message': 'product has been successfully deleted !',
						'data' : None
				}
		else:
			message = {
						'status': 0,
						'message': 'This product does not exists !',
						'data' : None
				}
	except:

		message = {
			'status': - 1,
			'message': 'Error !',
			'data' : None
		}

	return jsonify(message)

# List products
@app.route('/product/list' , methods = ['GET'])
def listProduct():
	try:
		products = Product.query.all()
		data = []
		for pr in products:
			data.append(pr.toJSON())


		message = {
					'status': 1,
					'message': 'Products list !',
					'data' : data
			}

	except:

		message = {
			'status': - 1,
			'message': 'Error !',
			'data' : None
		}

	return jsonify(message)