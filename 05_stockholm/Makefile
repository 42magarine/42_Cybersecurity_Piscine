build:	# Build the Docker containers
	docker build -t stockholm_image .

start:	# Start the Docker containers
	docker run -it --rm -v "$(shell pwd):/root" stockholm_image

clean:	# Remove the Docker image
	docker rmi stockholm_image
