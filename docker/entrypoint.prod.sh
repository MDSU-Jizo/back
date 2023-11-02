#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi


echo "[1/3] >>> Running migrations..."
python manage.py migrate
echo "[1/3] <<< Migration done"

echo "[2/3] >>> Importing datas into database..."
. /usr/src/.env
export PGPASSWORD=$POSTGRES_PASSWORD
psql --host=$POSTGRES_HOST --username=$POSTGRES_USER --dbname=$POSTGRES_DB -a -f ./init.sql
echo "[2/3] <<< Importation done"

echo "[3/3] >>> Creating super user..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$DJANGO_ADMIN_EMAIL', '$DJANGO_ADMIN_PASSWORD')" | python3 manage.py shell &>/dev/null
echo "[3/3] <<< Super User created"

exec "$@"