FROM python:3.6

# Setup
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /usr/src/app

# Add requirements separately to avoid re-installing module
# if no changes to requirements.txt
ADD requirements.txt /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt

# Add code and set the working directory
ADD . /usr/src/app
WORKDIR /usr/src/app/src
