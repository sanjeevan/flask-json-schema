.PHONY: wheel upload

clean:
	rm -rvf build
	rm -rvf dist
	rm -rvf Flask_json_schema.egg-info

wheel:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/* --skip-existing

