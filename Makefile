run:
	docker compose run -d test_bot#1

rebuild:
	docker compose build

clean:
	docker compose down
