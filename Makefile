start:
	docker-compose up

stop:
	docker-compose down

restart:
	docker-compose down && docker-compose up

startd:
	docker-compose up -d

restartd:
	docker-compose down && docker-compose up -d

logs:
	docker-compose logs -f

top:
	docker-compose top

collect:
	docker-compose exec backend python src/manage.py collectstatic --settings=app.settings.prod

shell:
	docker-compose exec backend python src/manage.py shell_plus --print-sql

export:
	export $(cat .env | sed 's/#.*//g' | xargs)
