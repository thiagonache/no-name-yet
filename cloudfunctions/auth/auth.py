import logging
import os
import jwt
from marshmallow import Schema, fields, validate, pre_load
from flask import abort, jsonify
from google.cloud import datastore, kms_v1
from google.cloud.kms_v1 import enums


def decrypt_symmetric(client, project_id, location_id, key_ring_id, crypto_key_id,
                      ciphertext):
    """Decrypts input ciphertext using the provided symmetric CryptoKey."""

    # The resource name of the CryptoKey.
    name = client.crypto_key_path_path(project_id, location_id, key_ring_id,
                                       crypto_key_id)
    # Use the KMS API to decrypt the data.
    response = client.decrypt(name, ciphertext)
    return response.plaintext


# BEGIN TO BECOME MODULE
def fetch_data(client, kind):
    query = client.query(kind=kind)
    entities = query.fetch()
    return entities


def check_user_exist(client, email):
    users = fetch_data(client, "users")
    for user in users:
        if user["email"] == email:
            return user
    return None


def validate_post(logger, request, schema):
    if request.method == "POST":
        content_type = request.headers['content-type']
        if content_type == 'application/json':
            request_json = request.get_json(silent=True)
            result = schema.load(request_json)
            if result.errors:
                logger.error(str(result.errors))
                abort(400)
            else:
                return result
        else:
            abort(400)
    else:
        abort(400)
# END TO BECOME MODULE


class AuthSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email(
        error='Not a valid email address'),)
    password = fields.Str(required=True, validate=[validate.Length(
        min=6, max=24, error="Password must have min of 6 and max of 24 characteres")])

    # Clean up data
    @pre_load
    def process_input(self, data):
        data['email'] = data['email'].lower().strip()
        return data


def auth(request):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('auth')

    # set headers and return 204 if options is the request method
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type, X-Auth-Token',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # handle payload
    schema = AuthSchema()
    result = validate_post(logger, request, schema)

    # Creates an API client for the Datastore API.
    datastore_client = datastore.Client(project=gcp_project)
    # Creates an API client for the KMS API.
    kms_client = kms_v1.KeyManagementServiceClient()

    # parse and manipule data
    data = result.data
    email = data["email"]
    key_ring_name = ''.join(e for e in email if e.isalnum())
    password = data["password"]

    # basic check
    user = check_user_exist(datastore_client, email)
    if user is not None:
        name = user["name"]
        enc_password = user["password"]
        dec_password = decrypt_symmetric(
            kms_client, gcp_project, "global", key_ring_name, "user_password", enc_password)
        if password == dec_password.decode():
            jwt_data = {
                "id": user.id, "name": name, "email": email, "role": "none"}
            jwt_encoded = jwt.encode(
                jwt_data, jwt_token, algorithm=jwt_algorithm)
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Expose-Headers': 'X-Auth-Token',
                'X-Auth-Token': jwt_encoded.decode()
            }
            logger.debug("%s authenticated" % email)
            return jsonify({"message": "User authenticated"}), 200, headers
        else:
            logger.error("password failed for user %s" % email)
            abort(403)
    else:
        logger.error("User does not exist")
        abort(403)


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

    @app.route('/auth', methods=["OPTIONS", "POST"])
    def index():
        return auth(request)

    app.run('127.0.0.1', 8000, debug=True)
