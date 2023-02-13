import pandas as pd
from flask import Flask, Response, render_template, request

app = Flask(__name__)
generator = pd.read_csv("static/simulations.csv").iterrows()

@app.route("/status")
def status():
    # refering to the global variable "generator"
    global generator
    value = next(generator, [None, None])[1]
    # if the dataframe is terminated, the "value" becomes None
    if (value is None):
        # restarting the generator for the beginning
        generator = pd.read_csv("static/simulations.csv").iterrows()
        value = next(generator, [None, None])[1]
    # creating the payload to be returned
    payload = str(value.to_json())
    return Response(payload)

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
