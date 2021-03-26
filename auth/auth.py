import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'capstone100.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Cap100'

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

'''
implement get_token_auth_header() method,
    it should attempt to get the header from the request it should raise an
    AuthError if no header is present
    it should attempt to split bearer and the token
    it should raise an AuthError if the header is malformed return the token
    part of the header
'''


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    auth = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxOS2pUb1dhVkNTamJaTWxvdFBxWCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lMTAwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDU3YWQ0NDE0NDZkOTAwNzFmMWJjMWUiLCJhdWQiOiJDYXAxMDAiLCJpYXQiOjE2MTY3OTk4NzEsImV4cCI6MTYxNjgwNzA3MSwiYXpwIjoiNnlSTXduck9KR1BDdmwzam5rR3pXMjVMb3Blc1FhUGEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.OCsW3l6M5PzZjPISoYCV8TcSe6L0GgNqU-gGYrtdyGSW5OP6rc_Ef9ILddRHcAntG5874zc7ktwNfMbYqk4x51vDXNb1l0aUVsnOn3t45iT_Y0IRGbd2CuJxPOUPe5Ned3goDk5jaggHvgleT-p46E1zOCuzKMDXsAVFDG1sieSZB1PvzSHxoq8BUTaXnp0HsyMJSoMi6P_fm5VX_blWEaLr0DRnh1ZT_DWEU2hrN5btQLVfgyGLw1LeLvLXS3zEXL-6fnKTw1RKixEDcZTgafB53YlL3KRamPi6fOl7nCxZP8Isl1qmDlhGVshRd_i20vWNA873DHOAokBtxl0rNw'
        }
    #auth = request.headers['Authorization']
    print("-----------------------------------------------------", auth)
    print("-----------------------------------------------------", auth)
    print("-----------------------------------------------------", auth)

    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    header_info = auth['Authorization'].split()
    if header_info[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(header_info) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(header_info) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = header_info[1]
    return token


'''
implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload
    it should raise an AuthError if permissions are not included in the payload
    !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in
    the payload permissions array return true otherwise
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'permissions_header_missing',
            'description': 'permissions header is expected.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'permission_is_missing',
            'description': 'permission is expected.'
        }, 403)
    return True


'''
implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)
    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload
    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
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
    if rsa_key:
        try:
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
                'description': 'Incorrect claims. Check audience and issuer.'
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


'''
implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the
    requested permission return the decorator which passes the decoded
    payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', token)
            try:
                payload = verify_decode_jwt(token)
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', payload)
                check_permissions(permission, payload)
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', permission)
            except Exception:
                abort(401)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
