.PHONY: install lint test docs

install:
	uv sync
	uv pip install -e .

lint:
	uv run ruff check tradestation/
	uv run ruff check tests/
	uv run mypy -p tradestation
	uv run mypy -p tests

test:
	uv run pytest --cov=tradestation --cov-report=term-missing tests/ --cov-fail-under=95

docs:
	cd docs; make html
