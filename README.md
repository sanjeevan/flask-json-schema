# Flask-json-schema

This extension makes it easy to validate JSON data that is sent to your Flask app using the jsonschema spec

## Setup

Flask-json-schema is available on PyPI and can be installed with

    pip install flask-json-schema

The extension can either be initialized directly:

```python
from flask import Flask
from flask_json_schema import JsonSchema

app = Flask(__name__)
schema = JsonSchema(app)
```

Or through the factory method:

```python
schema = JsonSchema()

app = Flask(__name__)
schema.init_app(app)
```

## Quick example

```python
from flask_json_schema import JsonSchema, JsonValidationError
from flask import Flask, jsonify, request

app = Flask(__name__)
schema = JsonSchema(app)

todo_schema = {
    'required': ['todo'],
    'properties': {
        'todo': { 'type': 'string' },
        'priority': { 'type': 'integer' },
    }
}

todos = []

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]})

@app.route('/todo', methods=['GET', 'POST'])
@schema.validate(todo_schema)
def create_message():
    if request.method == 'POST':
        todos.append( request.get_json() )
        return jsonify({ 'success': True, 'message': 'Created todo' })

    return jsonify(todos)

app.run('0.0.0.0', 5000, debug=True)
```

See `example.py` for the source code


## Links

* [Source Code](https://github.com/sanjeevan/flask-json-schema)
* [Issues](https://github.com/sanjeevan/flask-json-schema/issues)

