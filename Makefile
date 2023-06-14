exec-in-container = docker compose exec app

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

shell: up
	${exec-in-container} bash

format: up
	${exec-in-container} black .
	${exec-in-container} isort .

typecheck: up
	${exec-in-container} mypy .

patch:
	${exec-in-container} poetry version patch

minor:
	${exec-in-container} poetry version minor

major:
	${exec-in-container} poetry version major
