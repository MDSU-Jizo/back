# Jizo - BackEnd

:important: WORK IN PROGRESS :important:

## Before build

Create a .env file at the root of the project (Where the README is located) in which you will copy/paste then fill the content of the .env.sample file.
```dotenv
# .env.sample content

# DJANGO
DJANGO_SK= # You can find the value of this variable in the github project's secret variables

# POSTGRESQL
POSTGRES_USER=
POSTGRES_DB=
POSTGRES_PASSWORD=
```

## How to build

Build the project in detached mode and start the container.
```shell
docker compose up --build -d 
```

## How to build in production

```shell
docker compose -f docker-compose.prod.yaml up --build -d
```


## Connect to PostgresSQL using CLI

Using docker to execute the command that allows to connect to the database in your terminal
```shell
docker exec -it postgres psql -U <username> -d <database>
```