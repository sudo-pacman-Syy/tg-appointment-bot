run:
	docker compose run -d tg-appointment-bot

rebuild:
	docker compose build

clean:
	docker compose down
