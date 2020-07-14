from flask import Flask, render_template, request
import utils

app = Flask(__name__)


@app.route('/')
def homepage():
    return "penglv shi bendan"


if __name__ == "__main__":
    app.run()
