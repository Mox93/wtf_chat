from flask import Blueprint, render_template, send_file, url_for, request, redirect
import os


web = Blueprint("web", __name__)

ROOT_PATH = os.path.dirname(__file__)


@web.route("/avatar/<string:file_name>", methods=["GET", "POST"])
def avatar(file_name):
    if request.method == "POST":
        return 204

    file_path = ROOT_PATH + url_for("static", filename=f"avatar/{file_name}")

    try:
        return send_file(file_path)
    except Exception as e:
        print(str(e))
        return send_file(os.path.join(os.path.dirname(file_path), "default.svg"))


@web.route("/assets/<string:file_name>", methods=["GET"])
def assets(file_name):
    file_path = ROOT_PATH + url_for("static", filename=f"assets/{file_name}")
    return send_file(file_path)


@web.route("/", methods=["GET"])
def root():
    return render_template("index.html")


@web.route("/<path:url>", methods=["GET"])
def any_endpoint(url):
    return redirect(url_for("web.root"))
