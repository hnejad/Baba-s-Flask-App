from flask import Flask, render_template
from queryData import queryData, getHeaders

app = Flask(__name__)

@app.route("/")
def index():
    data = queryData()
    headers = getHeaders()
    return render_template("index.html",data=data, headers=headers)

if __name__ == "__main__":
    app.run(debug=1)