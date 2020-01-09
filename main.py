import os
import flask
from injector import Injector
from todo.bind import bind_todo

injector = Injector([])
injector.binder.install(bind_todo)

app = flask.Flask(__name__)


@app.route('/')
def root():
    dummy_todos = [
        {"name": "Buy a shampoo"},
        {"name": "Buy a tooth brush"}
    ]

    return flask.render_template('index.html', todos=dummy_todos)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
