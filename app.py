import pandas as pd
from flask import Flask, Response, render_template

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

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()