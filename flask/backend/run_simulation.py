from flask import Blueprint, render_template, request, session, flash, redirect
from callcenter.CallCenter import CallCenter
import threading
import json
simulationBP = Blueprint("simulation", __name__, static_folder="static", template_folder="templates")


@simulationBP.route("/run_simulation", methods=["GET", "POST"])
def main_page():
    if request.method == "GET":
        return render_template("simulation_results.html")

    elif request.method == "POST":
        user_params = request.form
        with open("../callcenter/user_parameters.json", "w") as f:
            json.dump(user_params, f, indent=4)
        cc = CallCenter()
        t1 = threading.Thread(target=cc.run)
        t1.start()
        return render_template("simulation.html")

    else:
        return render_template("error_page.html")