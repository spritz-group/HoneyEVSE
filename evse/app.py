import json
import logging
from flask import Flask, redirect, render_template, request

from gevent.pywsgi import WSGIServer

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
        if "page" in request.form:
            app.logger.info('Time spent on the page %s from %s: %s' ,
                        request.form['page'],
                        request.remote_addr,
                        request.form['timeOnPage'])
        else:
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
        if "page" in request.form:
            app.logger.info('Time spent on the page %s from %s: %s' ,
                        request.form['page'],
                        request.remote_addr,
                        request.form['timeOnPage'])
        else:
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
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        app.logger.info('Time spent on the page %s from %s: %s' ,
                        request.form['page'],
                        request.remote_addr,
                        request.form['timeOnPage'])
    return render_template("admin.html")

# Route for the user web interface
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if "page" in request.form:
            app.logger.info('Time spent on the page %s from %s: %s' ,
                            request.form['page'],
                            request.remote_addr,
                            request.form['timeOnPage'])
        if "action" in request.form:
            app.logger.info('%s by host %s' ,
                            request.form['action'],
                            request.remote_addr)
    return render_template("dashboard.html")

# Route for the info table"/dashboard",
@app.route("/", methods=['GET', 'POST'])
def info():
    if request.method == 'POST':
        app.logger.info('Time spent on the page %s from %s: %s' ,
                        request.form['page'],
                        request.remote_addr,
                        request.form['timeOnPage'])
    return render_template("info.html")


if __name__ == "__main__":
    # app.run(debug=True, port=8000)
    http_server = WSGIServer(("127.0.0.1", 8080), app)
    http_server.serve_forever()