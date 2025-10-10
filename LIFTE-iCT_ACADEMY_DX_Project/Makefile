SHELL := /bin/bash

up:
	docker compose -f infra/compose.yaml up --build

down:
	docker compose -f infra/compose.yaml down

migrate:
	docker compose -f infra/compose.yaml exec web python manage.py migrate

superuser:
	docker compose -f infra/compose.yaml exec web python manage.py createsuperuser

logs:
	docker compose -f infra/compose.yaml logs -f
