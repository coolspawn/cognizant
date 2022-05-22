DC_TEST = @docker-compose \
       --file docker-compose.test.yml
DC_DEV = @docker-compose \
       --file docker-compose.yml
DC_LOCAL = @docker-compose \
       --file docker-compose.local.yml

run_tests:
	$(DC_TEST) up --build

run_app:
	$(DC_DEV) up --build -d

# for local development. app running on host machine
run_env:
	$(DC_LOCAL) up --build -d

down_env:
	$(DC_LOCAL) down