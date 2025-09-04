# dev
run-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up

run-dev-d:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

run-dev-build:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

stop-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down

# prod
run-prod:
	docker compose up

run-prod-d:
	docker compose up -d

stop-prod:
	docker compose down
