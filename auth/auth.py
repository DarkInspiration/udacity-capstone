import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os


import os
# AUTH0_DOMAIN = 'darkinspiration.eu.auth0.com'
# ALGORITHMS = ['RS256']
# API_AUDIENCE = 'casting_agency_api'
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = [os.getenv('ALGORITHMS')]
API_AUDIENCE = os.getenv('API_AUDIENCE')

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

def get_token_auth_header():
    if 'Authorization' not in request.headers:
        abort(401)
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')
    if len(header_parts) != 2:
        abort(401)
    elif (header_parts[0]).lower() != 'bearer':
        abort(401)
    return header_parts[1]


def verify_decode_jwt(token):
    # Get public key from auth
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)
    # Choose our key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # Verify
    if rsa_key:
        try:
            # Use the key to validate the jwt
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Invalid claims. Check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


def check_permissions(permissions, payload):
    if 'permissions' not in payload:
        abort(400)
    if permissions not in payload['permissions']:
        abort(403)
    return True


def requires_auth(permissions=''):
    def requires_auth_decoratior(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            try:
                payload = verify_decode_jwt(jwt)
            except BaseException:
                abort(401)
            check_permissions(permissions, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decoratior
