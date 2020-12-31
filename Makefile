rm-volumes:
	docker volume ls --filter name=clustering.* -q | xargs docker volume rm