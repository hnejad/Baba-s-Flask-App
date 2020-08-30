from flask import Flask, render_template
from queryData import queryData

app = Flask(__name__)

@app.route("/")
def index():
    data = queryData()
    return render_template("index.html",data=data)

if __name__ == "__main__":
    app.run(debug=1)