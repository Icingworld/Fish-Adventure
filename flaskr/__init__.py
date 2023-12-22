import os
from flask import Flask, render_template, abort, redirect, url_for, request

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    @app.route("/")
    def home():
        ...

    from . import route
    level_count = 1
    for routes, pages in route.levels.items():
        exec(f"""
@app.route("{routes}")
def go_to_levels_{level_count}():
    session_id = request.cookies.get("SESSIONID")
    print(session_id)
    if session_id is None:
        # set sessionid
        ...
    # search sessionid's record
    if True:  # record >= level_count - 1
        # add sessionid's record
        return render_template("{pages}")
    else:
        return render_template("404.html")
             """)
        level_count += 1

    @app.route("/wuhu")
    def winner():
        ...

    @app.route("/rank")
    def rank():
        return render_template("rank.html")

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app