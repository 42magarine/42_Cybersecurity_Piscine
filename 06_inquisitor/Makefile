all: build up

build:
	docker-compose build

up:
	docker-compose up -d

bash1:
	docker exec -it ftp_server sh

bash2:
	docker exec -it ftp_client sh

bash3:
	docker exec -it attacker sh

down:
	docker-compose down

logs:
	docker-compose logs -f

nls:
	docker network ls

clean:
	docker-compose down -v --rmi all --remove-orphans
