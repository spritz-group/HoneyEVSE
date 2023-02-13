import json
from flask import Flask, render_template, request

app = Flask(__name__)

def generator_json(file_path=""):
    for obj in json.load(open(file_path)):
        yield obj

generator = generator_json("static/test.json")

# Route for request a new chargeS
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
        app.logger.info('Trying to login with username: %s and password: %s',
                        request.form['username'],
                        request.form['password'])
        error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()
