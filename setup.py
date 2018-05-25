import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-json-schema",
    version="0.0.1",
    author="Sanjeevan Ambalavanar",
    author_email="sanjeevan@pureparadox.com",
    license="MIT",
    description="Flask extension to validate JSON requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sanjeevan/flask-json-schema",
    packages=['flask_json_schema'],
    zip_safe=False,
    install_requires=[
        'Flask>=0.9',
        'jsonschema>=1.1.0'
    ],
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
