
IMAGE_NAME = kpmg_rag_llm_app
# Name of the Docker container
CONTAINER_NAME = kpmg_rag_llm_container
# Path to Dockerfile
DOCKERFILE_PATH = .
# Port to expose
PORT = 8080

# Build the Docker image
build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME) $(DOCKERFILE_PATH)

# Run the Docker container
run:
	@echo "Running Docker container..."
	docker run -d --name $(CONTAINER_NAME) --env-file .env -p $(PORT):$(PORT) $(IMAGE_NAME)

# Show logs from the running container
logs:
	@echo "Showing logs for Docker container..."
	docker logs -f $(CONTAINER_NAME)

# Build and then run the container
build-run: build run logs

# Stop the running container
stop:
	@echo "Stopping Docker container..."
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Clean up Docker resources (dangling images, stopped containers)
clean:
	@echo "Cleaning up Docker resources..."
	docker system prune -f

# Rebuild the image and restart the container
restart: stop build run

