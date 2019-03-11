#!/usr/bin/python

import logging
import os
from flask import abort, jsonify
from google.cloud import datastore
from marshmallow import Schema, fields, validate


gcp_project = os.getenv('GCP_PROJECT', None)
if gcp_project is None:
    raise Exception('Environment variable GCP_PROJECT is mandatory')


class PollSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False, validate=[validate.Length(
        max=100, error="Description must have max of 100 characteres")])


def fetch_data(client, kind):
    query = client.query(kind=kind)
    entities = query.fetch()
    return entities


def store_data(client, kind, data):
    entity = datastore.Entity(key=client.key(kind))
    entity.update(data)
    client.put(entity)
    return entity


def get_polls(client, kind):
    entities = fetch_data(client, kind)
    return entities


def check_poll_exist_by_name(client, pollName):
    polls = get_polls(client, "polls")
    for poll in polls:
        if poll["name"] == pollName:
            return poll
    return False


def polls(request):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('polls')

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type,X-Auth-Token',
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
        try:
            request.headers["X-Auth-Token"]
        except:
            abort(403)

        content_type = request.headers['content-type']
        if content_type == 'application/json':
            request_json = request.get_json(silent=True)
            schema = PollSchema()
            result = schema.load(request_json)
            if result.errors or result.data is None:
                abort(400)
            else:
                # Creates an API client for the Datastore API.
                datastore_client = datastore.Client(project=gcp_project)
                # parse and manipule data
                data = result.data
                # basic check
                entity = check_poll_exist_by_name(
                    datastore_client, data["name"])
                if entity is not False:
                    return jsonify({"errors": "Poll created already"}), 422, headers
                else:
                    # Creates new option
                    new_entity = store_data(datastore_client, "polls", data)
                    description = data.get("description") or ""

                    data = {
                        "id": new_entity.id,
                        "name": new_entity["name"],
                        "description": description
                    }
                    return jsonify({'items': [data]}), 200, headers
        else:
            logger.error("Content-Type %s is not valid" % content_type)
            abort(400)

    elif request.method == "GET":
        # TODO: enable filtering via query string by sending poll name or id (tbd)
        request_args = request.args
        poll_id = request_args.get("pollId")

        entities = get_polls(datastore_client, "polls")
        items = []
        for entity in entities:
            description = entity.get("description") or ""
            data = {
                "id": entity.id,
                "name": entity["name"],
                "description": description
            }
            if poll_id is None:
                items.append(data)
            else:
                if str(entity.id) == poll_id:
                    items.append(data)
        return jsonify({'items': items}), 200, headers


if __name__ == "__main__":
    # enable local testing using flask
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/polls', methods=["GET", "OPTIONS", "POST"])
    def index():
        return polls(request)

    app.run('127.0.0.1', 8000, debug=True)
