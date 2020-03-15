from flask import Flask, render_template,request, redirect, session, flash, Response
from datetime import datetime, date
from mysqlconnection import connectToMySQL 
from pytz import timezone
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'

@app.route("/")
def index():
	
	return render_template("main.html")

@app.route("/register", methods=["POST"])
def register():
	errors = {}
	if request.method == "POST":
		try:
			if  len(request.form['name']) < 3:
				flash("Name should be at least 3 characters")
			if  len(request.form['username']) < 3:
				flash("Username should be at least 3 characters")
			if len(request.form['password']) < 8:
				flash("Password should be at least 8 characters")
			if request.form['password'] != request.form['c_password']:
				flash("Passwords do not match")
		except Exception as e:
				flash("Unknown error")
		if '_flashes' in session.keys():
			return redirect('/')
		else:
			mysql = connectToMySQL()
			query = "INSERT INTO users (name, username, password,  date_hired, created_at) VALUES (%(name)s, %(username)s, %(password)s, %(date_hired)s,NOW());"
			data = {
				"name": request.form['name'],
				"username": request.form['username'],
				"password": request.form['password'],
				"date_hired": request.form['date_hired'],
			}
			mysql.query_db(query, data)
			flash("You just created your password " +  request.form['password'] + " and "+ request.form['username'])
			return redirect("/")


@app.route("/login", methods = ["POST"])
def login():
	errors = {}
	if request.method == "POST":
		try:
			if  len(request.form['username']) < 3:
				flash("Username should be at least 3 characters")
			if len(request.form['password']) < 8:
				flash("Password should be at least 8 characters")
		except Exception as e:
				flash("Unknown error")
		if '_flashes' in session.keys():
			return redirect('/')
		else:
			mysql = connectToMySQL()
			query = "SELECT * FROM users WHERE username = %(username)s LIMIT 1;"
			data = {
				"username": request.form['username'],
			}
			user = mysql.query_db(query, data)
			if user:
				try:
					mysql = connectToMySQL()
					query = "SELECT * FROM users WHERE username = %(username)s AND password = %(password)s LIMIT 1;"
					data = {
						"username": request.form['username'],
						"password": request.form['password'],
					}
					user = mysql.query_db(query, data)
					session['is_logged_in'] = True
					session['name'] = user[0]['name']
					session['user_id'] = user[0]['id']
					session['username'] = user[0]['username']
					return redirect("/dashboard")
				except Exception as e:
					flash("Invalid email and password combination")
					return redirect("/")
			else:
				flash( "Email does not exist in the database")
				return redirect("/")

@app.route("/dashboard", methods = ["GET"])
def dashboard():
	if 'is_logged_in' in session:
		if session['is_logged_in'] == True:
			try:
				mysql = connectToMySQL()
				query = "SELECT * FROM users WHERE id = %(id)s LIMIT 1;"
				data = {
					"id": session['user_id']
				}

				user = mysql.query_db(query, data)
			except Exception as e:
				flash("Invalid session")
				return redirect("/")
			# utc = date.today()
			mysql = connectToMySQL()
			query = "SELECT joins.id as joins_id, joins.wish_item_id as user_ids, users.id as user_id, wish_items.item_product as item_product, users.name as name, wish_items.created_at as created, joins.id as joins_id FROM joins LEFT JOIN wish_items ON wish_items.id = joins.wish_item_id LEFT JOIN users ON users.id = wish_items.user_id WHERE joins.user_id = %(id)s"
			data = {
					"id": session['user_id']
			}
			myWishlist = mysql.query_db(query,data)
			# all_others_id = []
			# if mytrips:
			# 	for my_trips in mytrips:
			# 		all_others_id.append(my_trips['user_id'])
			
			mysql = connectToMySQL()
			query = "SELECT *,users.id as user_id, wish_items.id as wish_items_id, wish_items.created_at as created FROM wish_items LEFT JOIN users ON users.id = wish_items.user_id WHERE wish_items.user_id !=  %(user_id)s;"
			data = {
					"user_id": session['user_id'],
			}
			others_wishlist = mysql.query_db(query,data)
			print(others_wishlist)
			return render_template("dashboard.html", user = user, myWishlist = myWishlist, others_wishlist = others_wishlist)
		else:
			flash("User is not logged in")
			return redirect("/")
	else:
		flash("User is not logged in")
		return redirect("/")

@app.route('/wish_items/<id>', methods=['GET'])
def wishlist(id):
	mysql = connectToMySQL()
	query = "SELECT * FROM wish_items WHERE wish_items.id =  %(id)s;"
	data = {
		"id":{id}
	}
	datails = mysql.query_db(query, data)
	mysql = connectToMySQL()
	query = "SELECT * FROM joins left join wish_items on wish_items.id = joins.wish_item_id left join users on users.id = joins.user_id  WHERE joins.wish_item_id =  %(id)s;"
	data = {
		"id":{id}
	}
	others = mysql.query_db(query, data)
	print(others)
	return render_template("wish_list.html",datails = datails, others = others)

@app.route('/delete', methods=['POST'])
def delete():
	mysql = connectToMySQL()
	query = "DELETE FROM wish_items WHERE user_id = %(user_id)s;" 
	data = {
			"user_id": request.form['user_id'],
		}
	mysql.query_db(query, data)
	flash("You just deleted!")
	return redirect('/dashboard')

@app.route('/wish_items/create', methods=['GET'])
def wish_items():
	return render_template("wish_items.html")

@app.route('/add', methods=['POST'])
def add():
	today = date.today()
	if request.method == "POST":
		try:
			if  len(request.form['item/product']) < 5:
				flash("Product should be at least 5 characters")
		except Exception as e:
			flash("Unknown error")
		if '_flashes' in session.keys():
			return redirect('/wish_items/create')
		else:
			mysql = connectToMySQL()
			query = "INSERT INTO wish_items (user_id, item_product, created_at) VALUES (%(user_id)s,%(item_product)s, NOW());"
			data = {
				"user_id": session['user_id'],
				"item_product": request.form['item/product'],
			}
			mysql.query_db(query, data)
			flash("You just created a new Product!")
			return redirect('/dashboard')

@app.route('/remove', methods=['POST'])
def remove():
	mysql = connectToMySQL()
	query = "DELETE FROM joins WHERE id = %(user_id)s;" 
	data = {
			"user_id": request.form['user_id'],
		}
	mysql.query_db(query, data)
	flash("You just Removed!")
	return redirect('/dashboard')

@app.route('/logout', methods=['GET'])
def logout():
	session.clear()
	return redirect("/")

@app.route('/join', methods=['POST'])
def joint():
	mysql = connectToMySQL()
	query = "INSERT INTO joins (user_id, wish_item_id, created_at) VALUES (%(user_id)s, %(wish_items_id)s, NOW());"
	data = {
		"user_id": session['user_id'],
		"wish_items_id":request.form['wish_items_id'],
	}
	join = mysql.query_db(query,data)
	flash("You just added to you wishlist!")
	return redirect('/dashboard')


if __name__ == "__main__":
	app.run(port=8000, debug=True)
