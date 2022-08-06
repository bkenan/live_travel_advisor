install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv test.py

lint:
	pylint --disable=R,C,no-value-for-parameter,no-member app.py

all: install lint test 
