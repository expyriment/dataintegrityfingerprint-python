.PHONY: install clean build

install:
	python3 setup.py install

build:
	python3 setup.py sdist bdist_wheel


clean:
		@rm -rf build \
			dist \
			dataintegrityfingerprint.egg-info \
