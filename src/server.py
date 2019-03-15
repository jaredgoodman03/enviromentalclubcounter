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

def renderScript(name):
	with open("mostwanted/" + name, "r") as file:
		lines = file.read().split("\n")
		fullName = lines[0]
		phone = lines[1]
		opener = lines[2]
		yes = lines[3]
		no = lines[4]
		img = lines[5]
		return render_template('scripttemplate.html', name=fullName, phone=phone, opener=opener, yes=yes, no=no, title=fullName, imgsrc=img)

@app.route("/supporter")
def supporter():
	return renderScript("supporter")

@app.route("/denier")
def denier():
	return renderScript("denier")

@app.route("/harris")
def harris():
	return renderScript("harris")

@app.route("/inslee")
def inslee():
	return renderScript("inslee")

@app.route("/orourke")
def orourke():
	return renderScript("orourke")

@app.route("/sanders")
def sanders():
	#☭☭☭☭☭☭☭☭☭☭☭☭
	return renderScript("sanders")

@app.route("/barrasso")
def barrasso():
	return renderScript("barrasso")

@app.route("/booker")
def booker():
	return renderScript("booker")

@app.route("/pelosi")
def pelosi():
	return renderScript("pelosi")

@app.route("/trump")
def trump():
	return renderScript("trump") # as if they don't get enough calls already

@app.route("/mcconnell")
def mcconnell():
	return renderScript("mcconnell")

@app.route("/wheeler")
def wheeler():
	return renderScript("wheeler")

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

@app.route("/mostwanted")
def mostwanted():
	return render_template('mostwanted.html')

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
	return render_template('results.html', form = "<option selected>Number of calls</option> <option>School</option> <option>Representatives</option>", body=toDisplay, title="Number of calls")

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
		return render_template('results.html', form = "<option>Number of calls</option> <option selected>School</option> <option>Representatives</option>", body=toDisplay, title="School")
		
	if page == "Representatives":
		people = getPeople()
		reps = []
		for person in people:
			for rep in person.reps:
				if not rep == "Other":
					if Counter(rep, 0) not in reps:
						reps.append(Counter(rep, 1))
					else:
						reps[reps.index(Counter(rep, 0))].count += 1
		reps.sort(reverse=True) 
		toDisplay = tableStyle + sectionStyle + "Name" + th + "# of Contacts" + sectionEnd
		for rep in reps:
			toDisplay += sectionStyle + rep.name + th + str(rep.count) + sectionEnd

		toDisplay += "</table>"
		return render_template('results.html', form = "<option>Number of calls</option> <option>School</option> <option selected>Representatives</option>", body=toDisplay, title="Representatives")
	return "Hello, world!"


@app.route('/entry', methods=['POST'])
def entry_post():
	name = request.form['name'].title()
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

	return render_template('thankyou.html', title="Log a contact")


if __name__=="__main__":
	app.run(host='0.0.0.0', port=80)
