###########
# BUILDER #
###########

# Pull official base image
FROM python:3.11.5 as builder

# Define the author
LABEL author="https://github.com/Maengdok" \
      maintainer="Maengdok" \
      version="0.0.0"

# Set work directory
WORKDIR /home/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install gcc

# Upgrade pip
RUN pip install --upgrade pip

# Install python dependencies
COPY ./requirements.txt .

# Copy files into workdir
COPY . .

# Wheel is a built-package format, and offers the advantage of not recompiling your software during every install.
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /home/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# Pull official base image
FROM python:3.11.5

# Create directory for the app user
RUN mkdir -p /home/python

# Create the python user
RUN addgroup --system python && adduser --system --ingroup python python

# Create the appropriate directories
ENV HOME=/home/python
ENV APP_HOME=/home/python/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

# Install dependencies
RUN apt-get update && apt-get install netcat-openbsd
RUN apt-get install -y postgresql-client

# Get files from builder instance to copy it inside
COPY --from=builder /home/src/app/wheels /wheels
COPY --from=builder /home/src/app/requirements.txt .

# Execute installations
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint.prod.sh
COPY ./docker/entrypoint.prod.sh $HOME/bin/entrypoint.prod.sh
RUN sed -i 's/\r$//g' $HOME/bin/entrypoint.prod.sh
RUN chmod +x  $HOME/bin/entrypoint.prod.sh

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R python:python $APP_HOME

# change to the app user
USER python

# run entrypoint.prod.sh
ENTRYPOINT ["/home/python/bin/entrypoint.prod.sh"]