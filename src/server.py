from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from person import Person

app = Flask(__name__)

def getPeople():
	names = os.listdir("log/")
	people = []
	for name in names:
		with open("log/" + name, "r") as file:
			lines = file.read().split("\n")
			toAdd = Person(name=name, school=lines[0])
			x = 1
			print(len(lines))
			while (x < len(lines)-1): # We subtract one at the end because of an empty line
				toAdd.log(lines[x], lines[x+1]) #if everything goes well this won't break idk though
				x += 2
			people.append(toAdd)

	people.sort(reverse=True)
	return people

@app.route("/")
def index():
	#print(getPeople()[0])
	return render_template('index.html')

@app.route("/entry")
def entry():
      return render_template('entry.html')

@app.route("/results")
def results():
	return render_template('results.html', people=getPeople())

@app.route("/names")
def names():
      return render_template('names.html')

@app.route('/entry', methods=['POST'])
def entry_post():
	name = request.form['name']
	rep = request.form['rep']
	school = request.form['school']
	contact = request.form['contact']

	print("New log!")
	print("Name: " + name)
	print("Rep: " + rep)
	print("School: " + school)

	if name == "":
		return render_template('entry.html', error="This field is required.")
	
	# 1 file in log folder for each person, file name is person's name,# order of lines goes like this:
	# school
	# rep's name
	# communication(call, email, letter, etc)
	if not name in (os.listdir("log/")):
		with open("log/" + name, "w+") as file:
			file.write(school + "\n" + rep + "\n" + contact + "\n")
	else:
		with open("log/" + name, "a+") as file:
			file.write(rep + "\n" + contact + "\n")

	return render_template('thankyou.html')

if __name__=="__main__":
      app.run()