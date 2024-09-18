.PHONY: venv lint test docs

venv:
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -e .
	#.venv/bin/pip install -r docs/requirements.txt

lint:
	.venv/bin/isort --check --diff tradestation/ tests/
	.venv/bin/flake8 --count --show-source --statistics tradestation/ tests/
	.venv/bin/mypy -p tradestation
	.venv/bin/mypy -p tests

test:
	.venv/bin/pytest --cov=tradestation --cov-report=term-missing tests/ --cov-fail-under=95

docs:
	cd docs; make html
