# ft_onion

docker-compose up -d
docker-compose down
docker-compose restart nginx
docker logs nginx-container
docker exec -it tor-container cat /var/lib/tor/hidden_service/hostname
