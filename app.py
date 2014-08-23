#!flask/bin/python
from flask import Flask, jsonify, request, render_template, redirect
from db import get_database_connection
import json

app = Flask(__name__)


"""UI Routes"""

@app.route('/')
def index():
	"""Display Users"""
	db = get_database_connection()
	db.execute('select * from unbabel_user')
	users = db.fetchall()
	return render_template('home.html', users=users)


@app.route('/create', methods = ['GET','POST'])
def create_user():
	"""Create User"""
	if request.method == 'POST':
		db = get_database_connection()
		name = request.form['name']
		email = request.form['email']
		db.execute("select id from unbabel_user order by id desc limit 1")
		primary_key = int(db.fetchall()[0][0])
		primary_key += 1 
		db.execute("insert into unbabel_user values(%d, '%s', '%s')" % (primary_key, name, email))

	return redirect('/')


"""API Route"""

@app.route('/api', methods = ['GET', 'POST', 'PATCH'])
def user_resource():
	"""Handle API HTTP Requests"""
	db = get_database_connection()

	if request.method == 'GET':
		db.execute('select * from unbabel_user')
		records = db.fetchall()

		"""Build dict of dicts, keyed on user id"""
		json_dict = {} 
		for record in records:  
			info_dict = {'name':record[1],'email':record[2]}
			json_dict[record[0]] = info_dict 

		return jsonify( json_dict ), 201

	elif request.method == 'POST':
		info = json.loads(request.data) #request.json is another option here
		name = info['name']
		email = info['email']
		db.execute("select id from unbabel_user order by id desc limit 1")
		primary_key = int(db.fetchall()[0][0])
		primary_key += 1
		db.execute("insert into unbabel_user values(%d, '%s', '%s')" % (primary_key, name, email))

		return jsonify( { 'primary_key':primary_key, 'name': name, 'email':email } ), 201

	elif request.method == 'PATCH':
		info = json.loads(request.data)
		user_id = int(info['user_id'])
		try:
			user_update = info['name']
			email_update = info['email']
		except AttributeError:
			pass
		db.execute("update unbabel_user set name = '%s', email = '%s' where id = %d" % (name, email, user_id))

		return jsonify( {'name':name, 'email':email} ), 201


"""Run server"""
if __name__ == '__main__':
	app.run(debug = True)



	