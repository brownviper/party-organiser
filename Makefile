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

