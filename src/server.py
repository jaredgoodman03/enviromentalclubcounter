from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)

@app.route("/")
def index():
      return render_template('index.html')

@app.route("/entry")
def entry():
      return render_template('entry.html')

@app.route("/results")
def results():
      return render_template('results.html')

@app.route("/names")
def names():
      return render_template('names.html')

@app.route('/entry', methods=['POST'])
def entry_post():
	name = request.form['name']
	rep = request.form['rep']
	school = request.form['school']

	print("New log!")
	print("Name: " + name)
	print("Rep: " + rep)
	print("School: " + school)

	if name == "":
		return render_template('entry.html', error="This field is required.")
	
	# 1 file in log folder for each person, file name is person's name,# order of lines goes like this:
	# rep's name
	# school
	# communication(call, email, letter, etc)
	
	with open("log/" + name, "w+") as file:
		file.write(rep + "\n" + school)
	return render_template('thankyou.html')

if __name__=="__main__":
      app.run()