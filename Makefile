H=localhost
P=8000

run:
	@PYTHONPATH=apps/bikes/ python ./main.py --host $(H) --port $(P) --app $(A)
