from flask import Flask, flash, redirect, render_template, request, session, abort

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


if __name__=="__main__":
      app.run()