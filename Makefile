SHELL := /bin/bash

# Thor solo
solo-up: #@ Start Thor solo
	docker compose -f ./docker-compose.solo.yml up -d --wait
solo-down: #@ Stop Thor solo
	docker compose -f ./docker-compose.solo.yml down

# PyTest
test:
	poetry run pytest
test-unit:
	poetry run pytest tests/unit
test-solo:
	poetry run pytest tests/solo
