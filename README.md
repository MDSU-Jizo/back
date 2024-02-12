# Jizo - BackEnd
[![codecov](https://codecov.io/gh/MDSU-Jizo/back/graph/badge.svg?token=WXSWLAGA9R)](https://codecov.io/gh/MDSU-Jizo/back)

## Requirements

- [ ] Docker

## Before build

Create a .env file at the root of the project (Where the README is located) in which you will copy/paste the content of the .env.sample file then fill.
> [!WARNING]
> If you have randomly generated password that contains symbols, set them between quotes in the .env file to avoid any error

## How to build

Build the project in detached mode and start the container.
```shell
docker compose up --build -d 
```

## How to build the production environment

Start with the following command:
```shell
docker compose -f docker-compose.prod.yaml up setup -d
```

The setup service will create all required users needed for [ELK](https://github.com/deviantony/docker-elk/tree/main) authentications to work.

> [!IMPORTANT]
> Wait few minutes until the setup finishes to set up users necessary for `ELK` authentication to work

Once the setup ended paste the following command:

```shell
docker compose -f docker-compose.prod.yaml up --build -d
```

## Connect to PostgresSQL using CLI

Using docker to execute the command that allows to connect to the database in your terminal
```shell
docker exec -it postgres psql -U <username> -d <database>
```

## How does it work
### Prod Environment

The production environment has the `ELK` containers which allow \
to listen to exceptions and logs returned by the app and the containers \
Once the production environment started, reach for the following url: `localhost:5601` 

> [!NOTE]
> This url will redirect you to the Kibana dashboard where you could find the logs and exceptions. \
> But before that it will prompt you to log in. 

### Verify if the database is working

> [!NOTE]
> Depending on the launched environment, be sure to call one of the following routes:

| dev environment | prod environment |
|-----------------|------------------|
| `locahost:8000` | `locahost:80`    |
