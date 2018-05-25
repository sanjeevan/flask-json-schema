.PHONY: wheel upload

wheel:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/* --skip-existing
