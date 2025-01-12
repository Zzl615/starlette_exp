build:
	git pull
	docker build -t dify-api api
	docker build -t dify-web --build-arg ZOE_ENV=production web

up:
	docker-compose -f docker-compose.prod.yaml up -d

logs:
	docker-compose -f docker-compose.prod.yaml logs -f --tail=100

dev:
	git pull
	docker build -t dify-web --build-arg ZOE_ENV=dev web
	docker build -t dify-api api
	cd docker && docker-compose up -d && docker-compose restart nginx
