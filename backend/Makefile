.PHONY: migrate seed-staging-from-csv transform

migrate:
	python -m alembic upgrade head

seed-staging-from-csv:
	@if [ -z "$(path)" ]; then \
		echo "Debe proporcionar el path al CSV: make seed-staging-from-csv path=data/tiros.csv"; \
		exit 1; \
	fi
	python - <<'PY'
from app.services.data_service import DataService
service = DataService()
rows = service.load_csv_to_staging("$(path)")
print(f"Filas cargadas a staging: {rows}")
PY

transform:
	python - <<'PY'
from pprint import pprint
from app.services.data_service import DataService
service = DataService()
result = service.transform_staging_to_final()
service.clear_staging()
pprint(result)
PY
