H=localhost
P=8000

run:
	@PYTHONPATH=src/apps/bikes/ python src/main.py --host $(H) --port $(P) --app $(A)

test:
	@PYTHONPATH=src/:src/apps/bikes/ python -m pytest tests/tests.py