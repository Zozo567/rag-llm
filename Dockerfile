FROM python:3.10-bookworm


WORKDIR /app

COPY . .

# Install sqlite3 (should already be up-to-date in bookworm)
RUN apt-get update && apt-get install -y \
    sqlite3 \
    libsqlite3-dev

# Clean up APT when done to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python -m pip --no-cache-dir install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "app.api:app", "--workers", "3", "--host", "0.0.0.0", "--port", "8080", "--reload"]