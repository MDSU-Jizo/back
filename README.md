# Jizo - BackEnd

> [!WARNING]
> WORK IN PROGRESS

## Before build

Create a .env file at the root of the project (Where the README is located) in which you will copy/paste then fill the content of the .env.sample file.
```dotenv
# .env.sample content
# DJANGO
DJANGO_SK= # You can find the value of this variable in the github project's secret variables
DEBUG= # true or false
ALLOWED_HOSTS= # list of allowed hosts using the following format: localhost,127.0.0.1
DJANGO_LOG_LEVEL= # One of the following: DEBUG, INFO, WARNING, ...

# POSTGRESQL
POSTGRES_USER=
POSTGRES_DB=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=

# ELASTIC SEARCH
ELASTICSEARCH_URL=
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

## How does it work
### Dev Environment

Dev environment has (not for long) the `ELK` containers which allow to listen to exceptions and logs returned by the app and the containers \
Once the dev environment started, reach for the following url: `localhost:5601` \
> [!NOTE]
> This url will redirect you to the Kibana dashboard where you could find the logs and exceptions.

### Prod Environment
> [!IMPORTANT]
> In the near future, the `ELK` containers will be moved from the dev environment to the production environment.

### Verify if the database is working

> [!NOTE]
> Whatever the launched environment, be sure to call one of the following routes:

| dev environment        | prod environment       |
|------------------------|------------------------|
| `locahost:9999/docker` | `locahost:8000/docker` |

This will result on creating and pushing an entity into the database. If the database has been created successfully during the build this will return a JsonResponse \
Here is a JsonResponse example:
```json
{
  "code": 200,
  "result": "success",
  "msg": "",
  "data": {
    "id": 1,
    "title": "test",
    "text": "Hello, world!"
  }
}
```
