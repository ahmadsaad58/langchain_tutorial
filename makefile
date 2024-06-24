pip-freeze:
	conda list --export > conda.txt 
	pip list --format=freeze > requirements.txt	