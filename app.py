import pandas as pd
from flask import Flask, Response, render_template

app = Flask(__name__)
generator = pd.read_csv("static/simulations.csv").iterrows()

@app.route("/status")
def status():
    payload = str(next(generator)[1].to_json())
    return Response(payload)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()