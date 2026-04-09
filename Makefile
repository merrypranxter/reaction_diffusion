.PHONY: install test lint format docs docker clean

install:
	pip install -e ".[all]"

test:
	pytest tests/ -v --cov=core --cov=models

test-quick:
	pytest tests/ -v -m "not slow and not benchmark"

lint:
	black --check .
	mypy core/ models/ --ignore-missing-imports

format:
	black .

docs:
	mkdocs serve

docs-build:
	mkdocs build

docker-build:
	docker build -t cdr:latest .

docker-run:
	docker run -v $(PWD)/outputs:/app/outputs cdr:latest types -o /app/outputs

benchmark:
	python -m tools.profiler --sizes 128 256 512 1024

profile:
	python -m cProfile -o profile.stats -m tools.parameter_scanner types -o outputs
	python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumtime').print_stats(20)"

api:
	python -m tools.api_server

interactive:
	python -m tools.interactive_explorer

clean:
	rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/ .mypy_cache/
	rm -f profile.stats benchmark_results.md
	find . -name "*.pyc" -delete
	find . -name "*.so" -delete
	find . -name "*.c" -delete  # Cython generated

publish: clean
	python -m build
	python -m twine upload dist/*
