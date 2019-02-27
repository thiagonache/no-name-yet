#!/usr/bin/python

import logging
import os
from flask import abort, jsonify
from google.cloud import datastore

gcp_project = os.getenv('GOOGLE_CLOUD_PROJECT', None)
if gcp_project is None:
    raise Exception('Environment variable GOOGLE_CLOUD_PROJECT is mandatory')


def fetch_entity(client, kind):
    query = client.query(kind=kind)
    entities = query.fetch()
    for entity in entities:
        # by design we have just one entity in this kind
        return entity


def store_data(client, entity, data):
    if entity is not None:
        entity.update(data)
        client.put(entity)
    else:
        abort(500)


def get(client, kind):
    entity = fetch_entity(client, kind)
    try:
        votes = entity["votes"]
    except:
        abort(500)
    return votes


def increment(client, kind):
    entity = fetch_entity(client, kind)
    try:
        votes = entity["votes"]
    except:
        votes = 0
    votes += 1
    data = {'votes': votes}
    store_data(client, entity, data)


def poll(request):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('poll')

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*',
        'ContentType': 'application/json'
    }

    datastore_client = datastore.Client(project=gcp_project)
    if request.method == "POST":
        content_type = request.headers['content-type']
        if content_type == 'application/json':
            request_json = request.get_json(silent=True)
            if request_json and 'vote' in request_json:
                vote = request_json['vote']
            else:
                abort(400)
        else:
            abort(400)
        if vote == "yes":
            increment(datastore_client, "votesYes")
        elif vote == "no":
            increment(datastore_client, "votesNo")
        else:
            abort(400)
        return jsonify({'msg': 'Vote counted'}), 200, headers

    elif request.method == "GET":
        request_args = request.args

        if request_args and request_args['vote']:
            vote = request_args['vote']
        else:
            abort(400)

        if vote == "yes":
            votes = get(datastore_client, "votesYes")
        elif vote == "no":
            votes = get(datastore_client, "votesNo")
        else:
            abort(400)
        return jsonify({'votes': votes}), 200, headers


if __name__ == "__main__":
    # enable local testing using flask
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/poll')
    def index():
        return poll(request)

    app.run('127.0.0.1', 8000, debug=True)
