def require_env(value):
    if value is None:
        raise ValueError('Env variables not found')
    return value
