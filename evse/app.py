import json
import logging
from flask import Flask, redirect, render_template, request

logging.basicConfig(filename='record.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s : %(message)s')

def generator_json(file_path=""):
    """ The function create a generator from a json file in order to handle sequential route calls. """
    for obj in json.load(open(file_path)):
        yield obj

generator = generator_json("static/charges.json")

app = Flask(__name__)

# Route for request a new charges
@app.route("/status")
def status():
    # refering to the global variable "generator"
    global generator
    value = next(generator, None)
    # if the list is terminated, the "value" becomes None
    if (value is None):
        # restarting the generator for the beginning
        generator = generator_json("static/charges.json")
        value = next(generator, None)
    # return the payloaded value
    return value

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        app.logger.info('Trying to login with email: %s and password: %s from %s',
                        request.form['email'],
                        request.form['password'],
                        request.remote_addr)
        error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

# Route that handles the signup page logic
@app.route("/register", methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        app.logger.info('Trying to register with name: %s, surname: %s, email: %s, password: %s, confirm_password: %s from %s',
        request.form['name'],
        request.form['surname'],
        request.form['email'],
        request.form['password'],
        request.form['confirm_password'],
        request.remote_addr)
        return redirect("/")
    return render_template("register.html", error = error)

# Route for the HMI
@app.route("/admin")
def admin():
    return render_template("admin.html")

# Route for the user web interface
@app.route("/home")
def home():
    return render_template("home.html")

# Route for the info table
@app.route("/")
def info():
    return render_template("info.html")


if __name__ == "__main__":
    app.run()
