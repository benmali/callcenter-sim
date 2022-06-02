from flask import Blueprint, request
import os

removePlotsBP = Blueprint("remove_plots", __name__, static_folder="static", template_folder="templates")


@removePlotsBP.route("/remove_plots", methods=["GET"])
def remove_plots():
    if request.method == "GET":
        os.remove("static/images/arrivals.png")
        os.remove("static/images/call_abandon.png")
        os.remove("static/images/chat_abandon.png")
        os.remove("static/images/calls_queue.png")
        os.remove("static/images/chats_queue.png")
        os.remove("static/images/call_wait.png")
        os.remove("static/images/chat_wait.png")
        os.remove("static/images/rest_wait.png")
        os.remove("static/images/chats.png")
        os.remove("static/images/calls.png")
        return ('', 204)


