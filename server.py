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
			query = "INSERT INTO users (name, username, password,created_at) VALUES (%(name)s, %(username)s, %(password)s,NOW());"
			data = {
				"name": request.form['name'],
				"username": request.form['username'],
				"password": request.form['password'],
			}
			mysql.query_db(query, data)
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
			query = "SELECT *,users.id as user_id FROM add_travels LEFT JOIN users ON users.id = add_travels.user_id WHERE users.id = %(id)s"
			data = {
					"id": session['user_id']
			}
			mytrips = mysql.query_db(query,data)

			all_others_id = []
			if mytrips:
				for my_trips in mytrips:
					all_others_id.append(my_trips['user_id'])
			
			mysql = connectToMySQL()
			query = "SELECT *,add_travels.id as travel_id FROM add_travels LEFT JOIN users ON users.id = add_travels.user_id WHERE add_travels.user_id NOT IN  %(all_others_id)s;"
			data = {
					"all_others_id": all_others_id,
			}
			others_trips = mysql.query_db(query,data)
			print(others_trips)
			return render_template("travels.html", user = user, mytrips = mytrips, others_trips = others_trips)
		else:
			flash("User is not logged in")
			return redirect("/")
	else:
		flash("User is not logged in")
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

@app.route('/destination/<id>', methods=['GET'])
def destination(id):
	mysql = connectToMySQL()
	query = "SELECT * FROM add_travels left join users on add_travels.user_id = users.id WHERE add_travels.id =  %(id)s;"
	data = {
		"id":{id}
	}
	trips_datails = mysql.query_db(query, data)
	return render_template("destination.html", trips_datails = trips_datails)


@app.route('/add_plan', methods=['GET'])
def add_plan():
	return render_template("add.html")

@app.route('/add', methods=['POST'])
def add():
	errors = {}
	today = date.today()
	if request.method == "POST":
		try:
			if  len(request.form['Destination']) < 5:
				flash("destination should be at least 5 characters")
			if  len(request.form['Description']) < 10:
				flash("Description should be at least 10 characters")

			if 	datetime.strptime(request.form['Travel_from'], "%Y-%m-%d").date() < today:
				flash("Travel date should be future-dated")
			if 	datetime.strptime(request.form['Travel_to'], "%Y-%m-%d").date() < datetime.strptime(request.form['Travel_from'], "%Y-%m-%d").date():
				flash("Travel date should not be before the travel date from")
		except Exception as e:
			flash("Unknown error")
		if '_flashes' in session.keys():
			return redirect('/add_plan')
		else:
			mysql = connectToMySQL()
			query = "INSERT INTO add_travels (user_id, Destination, Description, Date_from, Date_to, created_at) VALUES (%(user_id)s, %(Destination)s, %(Description)s, %(Travel_from)s, %(Travel_to)s,NOW());"
			data = {
				"user_id": session['user_id'],
				"Destination": request.form['Destination'],
				"Description": request.form['Description'],
				"Travel_from": request.form['Travel_from'],
				"Travel_to": request.form['Travel_to'],
			}
			mysql.query_db(query, data)
			flash("You just created a new event!")
			return redirect('/dashboard')



@app.route('/logout', methods=['GET'])
def logout():
	session.clear()
	return redirect("/")

@app.route('/join', methods=['POST'])
def joint():
	mysql = connectToMySQL()
	query = "INSERT INTO joins (user_id, add_travels_id, created_at) VALUES (%(user_id)s, %(travel_id)s, NOW());"
	data = {
		"user_id": session['user_id'],
		"travel_id":request.form['travel_id'],
	}
	join = mysql.query_db(query,data)
	flash("You just joined!")
	return redirect('/dashboard')


if __name__ == "__main__":
	app.run(port=8000, debug=True)
