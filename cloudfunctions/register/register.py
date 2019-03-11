import logging
import os
from marshmallow import Schema, fields, validate, pre_load
from flask import abort, jsonify
from google.cloud import datastore, kms_v1
from google.cloud.kms_v1 import enums

gcp_project = os.getenv('GCP_PROJECT', None)
if gcp_project is None:
    raise Exception('Environment variable GCP_PROJECT is mandatory')


class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True, validate=validate.Email(
        error='Not a valid email address'),)
    password = fields.Str(required=True, validate=[validate.Length(
        min=6, max=24, error="Password must have min of 6 and max of 24 characteres")])
    created_at = fields.DateTime(dump_only=True)

    # Clean up data
    @pre_load
    def process_input(self, data):
        data['email'] = data['email'].lower().strip()
        return data


def encrypt_symmetric(client, project_id, location_id, key_ring_id, crypto_key_id,
                      plaintext):
    """Encrypts input plaintext data using the provided symmetric CryptoKey."""

    # The resource name of the CryptoKey.
    name = client.crypto_key_path_path(project_id, location_id, key_ring_id,
                                       crypto_key_id)

    # Use the KMS API to encrypt the data.
    response = client.encrypt(name, plaintext)
    return response.ciphertext


def create_key_ring(client, project_id, location_id, key_ring_id):
    """Creates a KeyRing in the given location (e.g. global)."""

    # The resource name of the location associated with the KeyRing.
    parent = client.location_path(project_id, location_id)

    # The keyring object template
    keyring_name = client.key_ring_path(project_id, location_id, key_ring_id)
    keyring = {'name': keyring_name}

    # Create a KeyRing
    response = client.create_key_ring(parent, key_ring_id, keyring)

    # print('Created KeyRing {}.'.format(response.name))
    return response


def create_crypto_key(client, project_id, location_id, key_ring_id, crypto_key_id):
    """Creates a CryptoKey within a KeyRing in the given location."""

    # The resource name of the KeyRing associated with the CryptoKey.
    parent = client.key_ring_path(project_id, location_id, key_ring_id)

    # Create the CryptoKey object template
    purpose = enums.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    crypto_key = {'purpose': purpose}

    # Create a CryptoKey for the given KeyRing.
    response = client.create_crypto_key(parent, crypto_key_id, crypto_key)

    print('Created CryptoKey {}.'.format(response.name))
    return response


def decrypt_symmetric(client, project_id, location_id, key_ring_id, crypto_key_id,
                      ciphertext):
    """Decrypts input ciphertext using the provided symmetric CryptoKey."""

    # The resource name of the CryptoKey.
    name = client.crypto_key_path_path(project_id, location_id, key_ring_id,
                                       crypto_key_id)
    # Use the KMS API to decrypt the data.
    response = client.decrypt(name, ciphertext)
    return response.plaintext


def fetch_data(client, kind):
    query = client.query(kind=kind)
    entities = query.fetch()
    return entities


def store_data(client, kind, data):
    entity = datastore.Entity(key=client.key(kind))
    entity.update(data)
    client.put(entity)


def make_user(client, data):
    store_data(client, "users", data)


def check_user_exist(client, email):
    users = fetch_data(client, "users")
    for user in users:
        if user["email"] == email:
            return True
    return False


def register(request):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('register')

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

    headers = {
        'Access-Control-Allow-Origin': '*',
        'ContentType': 'application/json'
    }
    if request.method == "POST":
        content_type = request.headers['content-type']
        if content_type == 'application/json':
            request_json = request.get_json(silent=True)
            schema = UserSchema()
            result = schema.load(request_json)
            if result.errors:
                abort(400)
            else:
                # Creates an API client for the Datastore API.
                datastore_client = datastore.Client(project=gcp_project)
                # parse and manipule data
                data = result.data
                email = data["email"]
                key_ring_name = ''.join(e for e in email if e.isalnum())
                # basic check
                exist = check_user_exist(datastore_client, email)
                if exist:
                    return jsonify({"errors": "User registered already"}), 422, headers
                else:
                    # Creates an API client for the KMS API.
                    kms_client = kms_v1.KeyManagementServiceClient()

                    try:
                        key_ring = create_key_ring(
                            kms_client, gcp_project, "global", key_ring_name)
                    except Exception as e:
                        logger.error(str(e))
                        abort(500)
                    logger.debug(key_ring)
                    try:
                        crypto_key = create_crypto_key(
                            kms_client, gcp_project, "global", key_ring_name, "user_password")
                    except Exception as e:
                        logger.error(str(e))
                        abort(500)
                    logger.debug(crypto_key)

                    logger.info("Encrypting password")
                    try:
                        encrypted_password = encrypt_symmetric(
                            kms_client, gcp_project, "global", key_ring_name, "user_password", str.encode(data["password"]))
                    except Exception as e:
                        logger.error(str(e))
                        abort(500)
                    logger.info("Creating user")
                    data["password"] = encrypted_password
                    try:
                        make_user(datastore_client, data)
                        return jsonify({"message": "User registered"}), 200, headers
                    except Exception as e:
                        logger.info(str(e))
                        abort(500)
        else:
            abort(400)
    else:
        abort(400)


if __name__ == "__main__":
        # enable local testing using flask
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/register', methods=["OPTIONS", "POST"])
    def index():
        return register(request)

    app.run('127.0.0.1', 8000, debug=True)
