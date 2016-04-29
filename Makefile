run:
	foreman start

run_gunicorn:
	gunicorn app:App

run_flask:
	python app.py

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

release: package pip_release

package: clean
	python setup.py sdist

pip_release:
	twine upload dist/*

clean:
	rm -rf dist/
