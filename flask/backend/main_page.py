from flask import Blueprint, render_template, request, session, flash, redirect

mainBP = Blueprint("main_page", __name__, static_folder="static", template_folder="templates")


@mainBP.route("/", methods=["GET"])
def main_page():
    if request.method == "GET":
        session["sol"] = 0
        try:
            with open("backend/simulation_params.txt") as file:
                sim_params = file.readlines()
            params = {}
            for param in sim_params:
                curr_param = param.split(",")
                params[curr_param[0]] = list(map(str.strip, curr_param[1:]))

            return render_template("main_page.html", params=params)

        except FileNotFoundError:
            return render_template("error_page.html")

        except Exception:
            return render_template("error_page.html")

    else:
        return render_template("error_page.html")