FROM python:3.13

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Ensure the entrypoint script is executable and fix potential line-ending issues
RUN chmod +x /app/docker-entrypoint.sh && \
    sed -i 's/\r$//' /app/docker-entrypoint.sh 2>/dev/null || true

EXPOSE 8000

# Use sh to execute the entrypoint script to avoid permission problems
ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]