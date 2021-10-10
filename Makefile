DC = docker-compose -p address_book -f docker/docker-compose.yml
IMAGE_TAG ?= latest
DOCKERFILE_ARGS ?= -f docker/Dockerfile
TARGET_ENV ?= development

.PHONY: help
help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: build
build: ## Build the docker images needed to run the server
	docker build -t address_book_${TARGET_ENV}:${IMAGE_TAG} --target ${TARGET_ENV} ${DOCKERFILE_ARGS} .

.PHONY: server
server: ## Start the Django server through docker-compose
	${DC} up -d

.PHONY: shell
shell: ## Start a new container running a shell
	${DC} run --rm --entrypoint="/bin/sh" server

.PHONY: clean
clean: ## Stop and remove containers created by the docker-compose up command
	${DC} down

.PHONY: server-shell
server-shell: ## Start a shell inside the server container
	${DC} exec server /bin/sh

.PHONY: logs
logs: ## Show logs of all containers in the project
	${DC} logs -f

.PHONY: status
status: ## List containers and their running processes
	${DC} ps
	@echo
	${DC} top

.PHONY: db-shell
db-shell: ## Run a PostgreSQL shell
	${DC} run -e "PGPASSWORD=server" --rm --entrypoint="psql --host=db --dbname=server --user=server" db
