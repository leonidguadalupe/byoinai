.PHONY: pull-images deploy upgrade

build:
	docker-compose -f docker/docker-compose.yml build

pull:
	git pull origin master

up:
	docker-compose -f docker/docker-compose.yml up -d

down:
	docker-compose -f docker/docker-compose.yml down -V

deploy: down up

upgrade: pull deploy