SHELL := /bin/bash

tests-unit:
	docker compose exec api uv run pytest --no-header --disable-warnings --tb=short -s -vv tests/unit/

tests-api:
	docker compose exec api uv run pytest --no-header --disable-warnings --tb=short -s -v tests/api/

tests-ui:
	docker compose exec ui pytest --no-header --disable-warnings --tb=short -s -v tests/e2e/

tests:
	docker compose up api --build -d
	make tests-unit
	make tests-api
	docker compose down -v

load-elasticsearch:
	./scripts/import_es.sh

clean-elasticsearch-index:
	./scripts/clean_index.sh

load-fixtures:
	docker compose exec api python -m fixtures.load_all

load-all:
	make load-elasticsearch
	make load-fixtures

reset-all:
	docker compose down -v
	docker system prune -a --volumes --force
	sudo rm -rf .local/ .data/ .downloaded/
	
	sudo rm -rf api/.env api/.venv/ api/.cache/ api/src/.model
	cp api/.env.dist api/.env
	
	sudo rm -rf ui/.env ui/.venv/ ui/.cache/
	cp ui/.env.dist ui/.env
	
	sudo rm -rf admin/node_modules/
	
	sudo rm -rf esco-helper/.env esco-helper/node_modules/
	cp esco-helper/.env.dist esco-helper/.env

	mkdir -p .local

	uv venv --directory=.local/ .venv-api
	. .local/.venv-api/bin/activate && uv sync --directory=api --active && deactivate
	
	uv venv --directory=.local/ .venv-ui
	. .local/.venv-ui/bin/activate && uv sync --directory=ui --active && deactivate

	docker compose up --build --force-recreate