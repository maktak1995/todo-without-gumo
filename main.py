import os
import flask

from google.cloud import datastore

app = flask.Flask(__name__)

datastore_client = datastore.Client()


def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times


@app.route('/')
def root():
    dummy_todos = [
        {"name": "Buy a shampoo"},
        {"name": "Buy a tooth brush"}
    ]

    return flask.render_template('index.html', todos=dummy_todos)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
