from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from person import Person
import uuid
import logging
from scorecounter import Counter

app = Flask(__name__)
tableStyle = "<table style=\"border:1px solid black; border-collapse:collapse;\" >"
th = "<th style=\"border:1px solid black; border-collapse:collapse;\">"
sectionStyle = "<tr style= \"border:1px solid black; border-collapse:collapse;\" > " + th
sectionEnd = " </th> </tr> "

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
	print("In default results page")
	toDisplay = tableStyle + sectionStyle + "Name" + th + "# of Contacts" + sectionEnd
	people = getPeople()
	for person in people:
		toDisplay += sectionStyle + person.name + th + str(person.num) + sectionEnd
	toDisplay += " </table>"
	return render_template('results.html', form = "<option selected>Number of calls</option> <option>School</option> <option>Representatives</option>", body=toDisplay)

@app.route("/results", methods=['GET', 'POST'])
def post():
	page = request.form['resultsoption']
	print("Page: " + page)
	if page == "Number of calls":
		return results()

	if page == "School":

		people = getPeople()
		schools = []
		for person in people:
			if Counter(person.school, 0) not in schools:
				schools.append(Counter(person.school, person.num))
			else:
				schools[schools.index(Counter(person.school, 0))].count += person.num
		schools.sort(reverse=True)
		toDisplay = tableStyle + sectionStyle + "School" + th + "# of Contacts" + sectionEnd
		for school in schools:
			toDisplay += sectionStyle + school.name + th + str(school.count) + sectionEnd
		toDisplay += "</table>"
		return render_template('results.html', form = "<option>Number of calls</option> <option selected>School</option> <option>Representatives</option>", body=toDisplay)
		
	if page == "Representatives":
		people = getPeople()
		reps = []
		for person in people:
			for rep in person.reps:
				if Counter(rep, 0) not in reps:
					reps.append(Counter(rep, 1))
				else:
					reps[reps.index(Counter(rep, 0))].count += 1
		reps.sort(reverse=True) 
		toDisplay = tableStyle + sectionStyle + "Name" + th + "# of Contacts" + sectionEnd
		for rep in reps:
			toDisplay += sectionStyle + rep.name + th + str(rep.count) + sectionEnd

		toDisplay += "</table>"
		return render_template('results.html', form = "<option>Number of calls</option> <option>School</option> <option selected>Representatives</option>", body=toDisplay)
	return "Hello, world!"


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