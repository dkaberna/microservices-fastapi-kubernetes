docker_remove_dangling_images:
	docker images --filter "dangling=true" -q --no-trunc | xargs docker rmi

deploy:
	chmod +x deploy.sh
	sh -c ./deploy.sh