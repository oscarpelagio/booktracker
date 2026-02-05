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