FROM python:3.9

RUN mkdir -p /app
WORKDIR /app

# Copy folders
ADD . .

# Install packages
RUN pip install -U pip && pip install -r requirements.txt

# Run flask app
EXPOSE {{ cookiecutter.flask_port }}
ENV FLASK_APP="src/main.py" FLASK_DEBUG=1 FLASK_ENV=docker
