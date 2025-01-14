.PHONY: install lint test docs

install:
	uv sync
	uv pip install -e .

lint:
	uv run ruff format tradestation/ tests/
	uv run ruff check tradestation/ tests/
	uv run pyright tradestation/ tests/

test:
	uv run pytest --cov=tradestation --cov-report=term-missing tests/ --cov-fail-under=95

docs:
	uv run -m sphinx -T -b html -d docs/_build/doctrees -D language=en docs/ docs/_build/
