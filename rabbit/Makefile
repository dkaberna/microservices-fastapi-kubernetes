export PYTHONPATH := .


.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: docker_build
docker_build:			## Builds, (re)creates, and starts the container
						docker compose up -d --force-recreate --build

.PHONY: docker_up
docker_up:				## Builds and starts the container
						docker compose up -d

.PHONY: docker_start
docker_start:			## Starts existing container
						docker compose start

.PHONY: docker_down
docker_down:			## Stop the container
						docker compose down

.PHONY: docker_remove_dangling_images
docker_remove_dangling_images:	## Removes dangling docker images
								docker images --filter "dangling=true" -q --no-trunc | xargs docker rmi