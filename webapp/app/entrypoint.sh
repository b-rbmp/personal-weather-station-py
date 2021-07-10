#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Rodar manualmente quando necessário no production. Rodo sempre o migrate no dev
#python manage.py flush --no-input (DELETA TODAS A DATABASE)
python manage.py migrate # (FAZ A MIGRAÇÃO DO DJANGO)
# Para rodar manualmente docker-compose exec web python manage.py flush --no-input | docker-compose exec web python manage.py migrate

exec "$@"