# use the rest as arguments for targets
TARGET_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
# ...and turn them into do-nothing targets
$(eval $(TARGET_ARGS):;@:)

COMPOSE=docker-compose

help:		   		## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

checkout-dev:
	git submodule init
	git submodule update
	git submodule foreach 'git checkout dev && git pull origin dev'

# containers

start: 				## start all containers
	$(COMPOSE) -f docker-compose.yml up -d

start-foreground:
	$(COMPOSE) -f docker-compose.yml up

stop: 				## stop all containers
	$(COMPOSE) -f docker-compose.yml stop

ls: 				## list all containers
	$(COMPOSE) -f docker-compose.yml ps

rebuild: 			## force rebuild a specific container
	$(COMPOSE) -f docker-compose.yml build --force-rm $(TARGET_ARGS)

logs: 				## tail container logs (example: make logs extractor)
	$(COMPOSE) -f docker-compose.yml logs -f $(TARGET_ARGS)

exec: 				## Open a bash of a specific container (usage: make exec [container] [command_to_execute]) example: make exec sender sh ls -la
	$(COMPOSE) -f docker-compose.yml exec $(TARGET_ARGS)

bash: 				## Open a bash of a specific container (usage: make bash [container])
	$(COMPOSE) -f docker-compose.yml exec $(TARGET_ARGS) bash

clean: 				## Purge container, removes the container, image and volumes attached to it, use with caution (usage: make clean [container])
	$(COMPOSE) -f docker-compose.yml stop; $(COMPOSE) -f docker-compose.yml rm -svf

restart: 			## Restart a specific container (usage: make restart [container])
	$(COMPOSE) -f docker-compose.yml stop $(TARGET_ARGS) && $(COMPOSE) -f docker-compose.yml start $(TARGET_ARGS)

clean-restart: 			## Stop, Rebuild and start a specific container(usage: make clean-restart [container])
	$(COMPOSE) -f docker-compose.yml stop $(TARGET_ARGS) && $(COMPOSE) -f docker-compose.yml rm -f $(TARGET_ARGS) && $(COMPOSE) -f docker-compose.yml build --force-rm $(TARGET_ARGS) && $(COMPOSE) -f docker-compose.yml up -d


# local
format:				## run autoflake, ssort, isort, black on all directories
	@sh -c " \
		pdm run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place thisapp/**; \
		pdm run ssort thisapp/**; \
		pdm run isort thisapp/**; \
		pdm run black thisapp/**; \
		pdm run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place atumm-ext/**; \
		pdm run ssort atumm-ext/**; \
		pdm run isort atumm-ext/**; \
		pdm run black atumm-ext/**; \
	"

format-dir:			## run autoflake, ssort, isort, black on a specific directory
	@sh -c " \
		pdm run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place $(TARGET_ARGS)/**; \
		pdm run ssort $(TARGET_ARGS)/**; \
		pdm run isort $(TARGET_ARGS)/**; \
		pdm run black $(TARGET_ARGS)/**; \
	"

install:			## install dependencies (from lock file)
	pdm sync

test:					## run tests
	pdm install && STAGE=test pdm run pytest --capture=no -cov --cov-report html

testf:					## run test filtered by pattern
	STAGE=test pdm run pytest -k $(TARGET_ARGS)

new-svc:
	pdm run python atumm-ext/atumm-core/atumm/core/entrypoints/cli/commands.py create-service $(TARGET_ARGS)

new-rsc:			## create a new rest resource within a service (service_name, resource_name), ex: make new-resource user tokens
	pdm run python atumm/core/entrypoints/cli/commands.py create-rest-resource $(TARGET_ARGS)
