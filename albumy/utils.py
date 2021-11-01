from flask import current_app
from itsdangerous.jws import TimedJSONWebSignatureSerialier as Serializer
from itsdangerous import BadSignature, SignatureExpired


from albumy.extensions import db
from albumy.settings import Operations


def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {
        'id': user.id,
        'operation': operation
     }
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(user, token, operation):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False
    
    if operation != data.get('operation') or user.id != data.get('id'):
        return False
    
    if operation == Operations.CONFIRM:
        user.confirmed = True
    else:
        return False
    
    db.session.commit()
    return True


