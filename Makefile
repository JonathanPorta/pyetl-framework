run:
	foreman start

run_flask:
	gunicorn app:App

run_worker:
	python worker.py

deps: install_local_dev

install_local_dev:
	./scripts/localdev-setup.sh

setup_local_redis:
	./scripts/localdev-redis.sh

setup_heroku:
	./scripts/heroku-setup.sh

deploy: deploy_staging deploy_production

deploy_staging:
	./scripts/heroku-deploy-staging.sh

deploy_production:
	./scripts/heroku-deploy-production.sh
