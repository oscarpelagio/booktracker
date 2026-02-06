# ---- Env File: ----
env:
	cp .env.example .env

# ---- Docker: ----
build:
	docker compose up -d --build
up:
	docker compose up -d
down:
	docker compose down

# ---- Alembic Migrations: ----
migrate:
	docker exec -i backend alembic upgrade head

migration:
	@read -p "Nom de la migració: " name; \
	docker exec -i backend alembic revision --autogenerate -m "$$name"

downgrade:
	@read -p "Revisions a fer downgrade (ej: -1): " rev; \
	docker exec -i backend alembic downgrade $$rev

migration-history:
	docker exec -i backend alembic history --verbose

current-migration:
	docker exec -i backend alembic current