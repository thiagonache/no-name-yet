#!/usr/bin/python

import jwt
import logging
import os
from flask import abort, jsonify
from google.cloud import datastore
from marshmallow import Schema, fields, validate, post_load


class AnswerSchema(Schema):
    id = fields.Int(dump_only=True)
    pollId = fields.Int(required=True)
    description = fields.Str(required=False, validate=[validate.Length(
        min=4, max=100, error="Description must have min of 4 and max of 100 characteres")])
    votes = fields.Int(default=0)
    created_by = fields.Email(dump_only=True)

    @post_load()
    def change_dict_keys(self, data):
        data["poll_id"] = data.pop("pollId")
        return data


def fetch_data(client, kind):
    query = client.query(kind=kind)
    entities = query.fetch()
    return entities


def store_data(client, kind, data):
    entity = datastore.Entity(key=client.key(kind))
    entity.update(data)
    client.put(entity)
    return entity


def update_data(client, entity):
    client.put(entity)
    return entity


def get_answers(client, kind):
    entities = fetch_data(client, kind)
    return entities


def check_answer_exist_by_description(client, answerDescription):
    answers = get_answers(client, "answers")
    for answer in answers:
        if answer["description"] == answerDescription:
            return answer
    return False


def answers(request):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('answers')

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT',
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
            # get user data
            user = jwt.decode(
                request.headers["X-Auth-Token"], jwt_token, jwt_algorithm)
        except:
            abort(403)
        content_type = request.headers['content-type']
        if content_type == 'application/json':
            request_json = request.get_json(silent=True)
            schema = AnswerSchema()
            result = schema.load(request_json)
            if result.errors or result.data is None:
                logger.error(result)
                abort(400)
            else:
                # Creates an API client for the Datastore API.
                datastore_client = datastore.Client(project=gcp_project)
                # parse and manipule data
                data = result.data
                # basic check
                entity = check_answer_exist_by_description(
                    datastore_client, data["description"])
                if entity is not False:
                    return jsonify({"errors": "Answer created already"}), 422, headers
                else:
                    # always initialize votes with zero
                    data["votes"] = 0

                    # adds created_by from jwt data
                    data["created_by"] = user["email"]

                    # Creates new answer
                    new_entity = store_data(datastore_client, "answers", data)

                    data = {
                        "id": new_entity.id,
                        "description": new_entity["description"],
                        "created_by": new_entity["created_by"],
                        "votes": 0
                    }
                    return jsonify({'items': [data]}), 200, headers
        else:
            logger.error("Content-Type %s is not valid" % content_type)
            abort(400)

    elif request.method == "GET":
        request_args = request.args
        try:
            pollId = request_args["pollId"]
        except:
            abort(400)

        entities = get_answers(datastore_client, "answers")
        items = []
        for entity in entities:
            if str(entity["poll_id"]) == pollId:
                data = {
                    "id": entity.id,
                    "description": entity["description"],
                    "created_by": entity["created_by"],
                    "votes": entity["votes"]
                }
                items.append(data)
        return jsonify({'items': items}), 200, headers

    elif request.method == "PUT":
        request_args = request.args
        try:
            answerDescription = request_args["description"]
        except:
            logger.info("Invalid query string")
            abort(400)

        entity = check_answer_exist_by_description(
            datastore_client, answerDescription)
        if entity is not False:
            entity["votes"] += 1
            updated_entity = update_data(datastore_client, entity)
            data = {
                "id": updated_entity.id,
                "description": updated_entity["description"],
                "votes": updated_entity["votes"],
                "created_by": updated_entity["created_by"]
            }

            return jsonify({'items': data}), 200, headers
        else:
            logger.info("Answer does not exist")
            abort(400)


def get_env_var(var, default=None):
    value = os.getenv(var, default)
    if value is None:
        raise Exception('Environment variable %s is mandatory' % var)
    else:
        return value


gcp_project = get_env_var('GCP_PROJECT')
jwt_token = get_env_var('JWT_TOKEN')
jwt_algorithm = get_env_var('JWT_ALGORITHM', 'HS256')

if __name__ == "__main__":
    # enable local testing using flask
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/answers', methods=["GET", "OPTIONS", "POST", "PUT"])
    def index():
        return answers(request)

    app.run('127.0.0.1', 8000, debug=True)
