from flask import Blueprint, render_template, request, session, flash, redirect

simulationBP = Blueprint("simulation", __name__, static_folder="static", template_folder="templates")


@simulationBP.route("/run_simulation", methods=["GET"])
def main_page():
    if request.method == "GET":
        session["sol"] = 0
        return render_template("simulation.html")

    elif request.method == "POST":
        session["sol"] = 0
        return render_template("simulation.html")

    else:
        return render_template("error_page.html")