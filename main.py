import os
import flask
from todo.application import injector
from todo.bind import bind_todo
from todo.presentation import register_views

injector.binder.install(bind_todo)

app = flask.Flask(__name__)
blueprint = flask.Blueprint("blueprint", __name__)
register_views(blueprint=blueprint)
app.register_blueprint(blueprint=blueprint)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
