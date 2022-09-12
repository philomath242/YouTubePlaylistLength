from cgitb import reset
from flask import Flask
from flask import Flask, render_template, request, redirect
from compute import compute

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", result="", url="")
    elif request.method == "POST":
        url = request.form["link"]
        (h, m, s) = compute(url)

        res = {h: "hours", m: "minutes", s: "seconds"}

        new_res = {}
        print(res)
        for k in res:
            if k != 0:
                new_res[k] = res[k]

        for t in new_res:
            if t == 1:
                new_res[t] = new_res[t][:-1]

        res_str = ""
        for k in new_res:
            res_str += str(k) + " " + new_res[k] + " "

        return render_template("index.html", result=res_str, url=url)


if __name__ == "__main__":
    app.run(debug=True)
