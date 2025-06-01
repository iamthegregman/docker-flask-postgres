FROM python:3.9-alpine

WORKDIR /home/app/

# Install dependencies
RUN apk add --no-cache postgresql-dev gcc musl-dev

# Copy and install requirements
COPY ./app/requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt

# Copy application code
COPY ./app /home/app/

# Copy .env file from root to container
COPY ./.env /home/app/.env


EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]