import db
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    list = db.get_neighborhood_list()
    return render_template("index.html", list = list)

@app.route("/result", methods=["POST"])
def result():
    parameters = {}
    data = request.form
    parameters["neighborhood"] = data["neighborhood"]
    parameters["date"] = data["date"]

    is_created = db.search_results(data["neighborhood"], int(data["date"]))

    if is_created:
        return render_template("result.html", parameters = parameters, research = is_created)
    else:
        list = db.get_neighborhood_list()
        error_message = "No se encontraron resultados, intenta con otros datos"
        return render_template("index.html", list = list, error_message = error_message)


app.run(host='localhost', port=5069, debug=True)