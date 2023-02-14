import json
from flask import Flask, render_template, request

app = Flask(__name__)

def generator_json(file_path=""):
    for obj in json.load(open(file_path)):
        yield obj

generator = generator_json("static/charges.json")

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
        app.logger.info('Trying to login with email: %s and password: %s',
                        request.form['email'],
                        request.form['password'])
        error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route("/")
def home():
    return render_template("home.html")

#route that handles the signup page logic
@app.route("/register", methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        app.logger.info('Trying to register with name: %s, surname: %s, email: %s, password: %s, confirm_password: %s',
        request.form['name'],
        request.form['surname'],
        request.form['email'],
        request.form['password'],
        request.form['confirm_password'])
    return render_template("register.html", error = error)

if __name__ == "__main__":
    app.run()
