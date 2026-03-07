start-env:
	uv venv --python 3.13.0 --clear
	uv sync
	echo "run the following command '''source .venv/bin/activate'''"

migrate:
	alembic upgrade head

fill-test-data:
	export PYTHONPATH="$$PWD:$$PYTHONPATH"; \
	echo "Building in $$PYTHONPATH";
	python party_app/initial_data/load_initial_data_to_db.py

run-server:
	fastapi dev party_app/main.py

run-tailwind:
	npm run tailwind:dev

test:
	python -m pytest "party_app/tests" -rP -vv -p no:warnings

wipe-all-containers:
	docker container prune
	docker image prune -a -f
	docker volume prune -a -f
	docker builder prune
	docker system df

start-containers:
	docker build . -t party_organizer
	docker run -d -p 8000:8000 --name party_app -e PORT=8000 party_organizer

start-containers-with-uv:
	docker build . -t party_organizer -f Dockerfile-uv
# 	docker run -d -p 8000:8000 --name party_app -e PORT=8000 party_organizer
