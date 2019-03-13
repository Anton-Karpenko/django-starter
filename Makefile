coverage:
	coverage run -m pytest
coverage-report:
	coverage report -m
server:
	python manage.py runserver
migrate:
	python manage.py migrate
migrations:
	python manage.py makemigrations