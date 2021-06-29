.PHONY: install clean build

build:
	python3 setup.py sdist bdist_wheel

install:
	python3 setup.py install

publish_test:
	twine check dist/*
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish:
	twine check dist/*
	twine upload dist/*

clean:
		@rm -rf build \
			dist \
			dataintegrityfingerprint.egg-info \
