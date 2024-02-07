up:
	docker compose up -d

down:
	docker compose down

flask:
	python3 ./webapp/app.py

kill:
	kill -9 $(lsof -i tcp:5000 | awk 'NR > 1 {print $2}')

pid:
	lsof -i tcp:5000 


