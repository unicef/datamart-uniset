lint:
	pipenv run pre-commit run --all-files
	pipenv run pre-commit run --all-files --hook-stage push
	pipenv run pre-commit run --all-files --hook-stage manual

clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage coverage.xml .eggs ./~build
	find src -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find tests -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf


fullclean:
	rm -fr .tox .cache .pytest_cache .venv
	$(MAKE) clean
