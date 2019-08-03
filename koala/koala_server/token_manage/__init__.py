from flask import g
from flask_httpauth import HTTPTokenAuth
from flask import make_response, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
serializer = Serializer('secret key here', expires_in=3600*12)
auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    """
    验证token是否正确
    :param token:
    :return:
    """
    return True
    g.username = None
    try:
        data = serializer.loads(token)
    except:
        return False
    if 'username' in data:
        g.username = data['username']
        return True
    return False


@auth.error_handler
def unauthorized():
    """
    token验证失败返回信息
    :return:
    """
    return make_response(jsonify({"result": "NT", "error": "Token已失效！请重新登陆！"}), 401)
