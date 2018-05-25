from functools import wraps
from flask import current_app, request
from jsonschema.validators import validator_for

class JsonValidationError(Exception):
    def __init__(self, message, errors):
        self.message = message
        self.errors = errors

class JsonSchema(object):

    def __init__(self, app):
        self.app = app
        self.config = {}
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.config = app.config.copy()
        self.config.setdefault('JSON_SCHEMA_METHODS', ['POST', 'PUT', 'PATCH'])
        self.config.setdefault('JSON_SCHEMA_FORMAT_CHECKER', None)

    def validate(self, schema, methods=None, format_checker=None):
        validator_kwargs = {
            'schema': schema,
            'format_checker': format_checker if format_checker else self.config.get('JSON_SCHEMA_FORMAT_CHECKER')
        }
        if not methods:
            methods = self.config.get('JSON_SCHEMA_METHODS')

        def wrapper(fn):
            @wraps(fn)
            def decorated(*args, **kwargs):
                if request.method in methods:
                    validator_cls = validator_for(schema)
                    validator = validator_cls(**validator_kwargs)
                    errors = list(validator.iter_errors(request.get_json()))
                    if errors:
                        raise JsonValidationError('Error validating against schema', errors)
                return fn(*args, **kwargs)
            return decorated
        return wrapper

