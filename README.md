# Track and Trace API

## Overview

The Track and Trace API exposes shipment and article information along with corresponding weather information.
I'm using the [openweathermap](https://home.openweathermap.org/) API to get the weather information. Before running the application, make you sign up to get an API key.

## Installation

You'll need to complete a few installation steps to run the API.

### Set up Python

The Track and Trace API is a Python application, so you'll need a working Python environment to run it.

### Python Version

The API currently requires Python >= 3.9.

### Create a Virtual Environment
It's recommended to create and activate a virtual environment before installing dependencies.

Python offers a built-in method for installing lightweight virtual environments, the `venv` module. To create a virtual environment with this command:

```shell
$ python3 -m <path to virtual environment>
```

After you've created your new virtual environment, you'll need to activate it in order to ensure subsequent commands use it instead of your system's default Python environment.

```shell
$ source .venv/bin/activate
```
### Install Dependencies
After you've created your virtual environment, you'll want to ensure that the correct dependencies are installed.

Run the pip command below to instead dependencies

```shell
 $  pip install -r requirements.txt
```
### Initialize Pre-Commit Hooks in the Repository

To configure git to use the API's configured pre-commit hooks (defined in [.pre-commit-config.yaml](.pre-commit-config.yaml)).

### Install the Pre-Commit Hook Package with Pip

```shell
$ python3 -m pip install pre-commit

$ pre-commit install
```

### Set up Docker

While you can easily perform some tasks (like testing) in a local virtual environment, it is recommended to set up Docker. You can [find instructions to install Docker here](https://docs.docker.com/engine/install/).

### Set up Docker Compose

Docker Compose is a tool for orchestrating Docker containers. If you have installed Docker Desktop, you already have Docker Compose installed. However, if you need to separately install Docker Compose, you can [find instructions for installing it here](https://docs.docker.com/compose/install/).

##### Build the database and API containers

If you've never built the API container before (and therefore don't have any build caches in place). Before running the command below, update the WEATHER_API_KEY field in the docker-compose file.

```shell
$ docker compose up
```
#### Run Database Migrations

To connect to the API container and execute the database migrations, run:

```shell
$ docker compose exec app alembic upgrade head
```

## Starting the API using Docker

If you're using Docker containers, just make sure container is online:

```shell
$ docker compose up
```

## Start API manually


0. **Install Required Packages**

Install dependencies using the command given above

2. **Create A Database**

In order to perform migrations and run the app, you'll need to create a database.
you should create a database called `trackandtrace`
To do this, you can use the [Postico](https://eggerapps.at/postico/) app or any other Postgresql client of your choice.

2. **Copy `.env` & set correct values**

The easiest way to set all environment variables needed for the API is to copy from sample:

$ cp .env_sample .env

The most important thing is to set DATABASE_URL. DATABASE_URL is mandatory and must be set to successfully run the API.

3. **Copy `alembic.ini` & check sqlalchemy.url**

In order for alembic to successfully run migrations, you'll need to update the `sqlalchemy.url` line in `alembic.ini`. An example of `alembic.ini` has been provided at `alembic.ini.example`. If you haven't already added your own version of this file, run the following command:

$ cp alembic.ini.example alembic.ini


Then, open `alembic.ini` in your editor of choice and ensure `sqlalchemy.url` line is EMPTY. It should look like this:


sqlalchemy.url =


4. **Run Database Migrations**

To create the database tables required by this app, the alembic library is provided. It has already been initialized, and if you have updated the `alembic.ini` file as specified above, you should be able to perform the latest database migrations by simply running:


$ alembic upgrade head


Please keep in mind that these migrations may remove all data from the database and set everything up from zero, so this particular command should never be used in a production environment or in any scenario where you wish for data to persist.

5. **Run Application**

To run the application, run the following:

```shell

$ python main.py
```
NOTE: make sure you have your radis server running, by running the command below:
```shell
$ redis-server
```

### Running tests

You can test by running the command. Make you have your database set-up before running the command below.

```shell
$ pytest
```

###

## API Documentation

Once the application is running, you can view the API documentation by opening [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) in the web browser of your choice.
