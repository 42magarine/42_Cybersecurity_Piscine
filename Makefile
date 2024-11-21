NGINX_CONTAINER = nginx-container
TOR_CONTAINER = tor-container

build:	# Build the Docker network and containers
	docker-compose build

start:	# Start the Docker containers
	docker-compose up -d

stop:	# Stop the Docker containers
	docker-compose down

show_onion:	# Show the .onion address
	@echo "Fetching .onion address..."
	@docker exec -it $(TOR_CONTAINER) cat /var/lib/tor/hidden_service/hostname

logs_nginx:	# Show the logs of the Nginx container
	docker logs $(NGINX_CONTAINER)

logs_tor:	# Show the logs of the Tor container
	docker logs $(TOR_CONTAINER)

status:	# Show the status of both containers
	@docker ps -a

clean:	# Clean up stopped containers and unused networks
	docker-compose down --volumes --remove-orphans

restart:	# Restart the Docker containers
	docker-compose restart

access_nginx:	# Access the Nginx container's shell
	docker exec -it $(NGINX_CONTAINER) /bin/sh

access_tor:	# Access the Tor container's shell
	docker exec -it $(TOR_CONTAINER) /bin/bash
