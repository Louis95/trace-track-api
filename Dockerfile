# Base image with Python 3.9 and dependencies
FROM python:3.9-slim-buster AS base

RUN apt-get update \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home Track-and-Trace-API \
    && chown -R Track-and-Trace-API /home/Track-and-Trace-API
WORKDIR /home/Track-and-Trace-API

USER Track-and-Trace-API

ENV PATH="/home/Track-and-Trace-API/.local/bin:$PATH"

COPY --chown=Track-and-Trace-API requirements.txt .

WORKDIR /Track-and-Trace-API

COPY --chown=Track-and-Trace-API . .


EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt



# Start the app
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
