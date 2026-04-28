run:
	docker compose up -d 

rebuild:
	docker compose build

clean:
	docker compose down
