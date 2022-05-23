DC_TEST = @docker-compose \
       --file docker-compose.test.yml
DC_DEV = @docker-compose \
       --file docker-compose.yml
DC_LOCAL = @docker-compose \
       --file docker-compose.local.yml

DC_CLUSTER = @docker-compose \
       --file docker-compose.cluster.yml

run_tests:
	$(DC_LOCAL) down -v
	$(DC_TEST) up --build

run_app:
	$(DC_DEV) up --build -d

run_cl_app:
	$(DC_CLUSTER) up --build -d

drop_cl_app:
	$(DC_CLUSTER) down -v --remove-orphans
# for local development. app running on host machine
run_env:
	$(DC_LOCAL) up --build -d

down_env:
	$(DC_LOCAL) down

drop_env:
	$(DC_LOCAL) down -v

tests: run_tests