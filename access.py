from flask import session, request, current_app
from functools import wraps


def group_permission_validator(config: dict, sess: session, r: request):
    group_name = sess.get('group_name', 'unauthorised')
    target_app = "" if len(r.endpoint.split('.')) == 1 else r.endpoint.split('.')[0]
    if group_name in config and target_app in config[group_name]:
        return True
    else:
        return False


def login_permission_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['PERMISSION_CONFIG']
        if group_permission_validator(config, session, request):
            return f(*args, **kwargs)
        else:
            return 'Group permission denied'
    return wrapper
