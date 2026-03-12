SHELL := /bin/bash

.PHONY: solo-up solo-down test test-unit test-solo

# Thor solo
solo-up: #@ Start Thor solo
	docker compose -f ./docker-compose.solo.yml up -d --wait
solo-down: #@ Stop Thor solo
	docker compose -f ./docker-compose.solo.yml down

# PyTest
test: #@ Run all tests with term, HTML, and XML coverage reports
	poetry run pytest --cov=thorix --cov-report=term-missing --cov-report=html --cov-report=xml
test-unit:
	poetry run pytest tests/unit
test-solo:
	poetry run pytest tests/solo
