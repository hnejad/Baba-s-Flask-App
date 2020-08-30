from flask import Flask, render_template
from queryData import getQueries

app = Flask(__name__)

@app.route("/")
def index():
    queries = getQueries()
    return render_template("index.html",queries=queries)

if __name__ == "__main__":
    app.run(debug=1)