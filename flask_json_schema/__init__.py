from functools import wraps, partial, update_wrapper
from flask import current_app, request
from jsonschema.validators import validator_for

class JsonValidationError(Exception):
    def __init__(self, message, errors):
        self.message = message
        self.errors = errors

class JsonSchema(object):

    def __init__(self, app=None):
        self.app = app
        self.config = {}
        self.validator_cls = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.config = app.config.copy()
        self.config.setdefault('JSON_SCHEMA_METHODS', ['POST', 'PUT', 'PATCH'])
        self.config.setdefault('JSON_SCHEMA_FORMAT_CHECKER', None)

    def validate(self, schema, methods=None, format_checker=None):
        def wrapper(fn):
            @wraps(fn)
            def decorated(methods=None, format_checker=None, *args, **kwargs):
                validator_kwargs = {
                    'schema': schema,
                    'format_checker': format_checker if format_checker else self.config.get('JSON_SCHEMA_FORMAT_CHECKER')
                }

                # use default methods if not supplied as arguments to decorator
                if not methods:
                    methods = self.config.get('JSON_SCHEMA_METHODS')

                # check jsonschema
                if request.method in methods:
                    validator_cls = self.validator_cls if self.validator_cls else validator_for(schema)
                    validator = validator_cls(**validator_kwargs)
                    errors = list(validator.iter_errors(request.get_json()))
                    if errors:
                        raise JsonValidationError('Error validating against schema', errors)

                return fn(*args, **kwargs)

            # the wrapper() func ctx has access to format_checker & methods, but the decorator
            # won't, so we use partial, where those args are passed in
            pfunc = partial(decorated, format_checker=format_checker, methods=methods)

            # this is needed because partial() doesn't add in __name__ attribute to the created
            # partial function, which Flask requires
            update_wrapper(pfunc, decorated)

            return pfunc

        return wrapper

