#!/bin/bash
# Docker entrypoint script that routes to either console or API based on MODE environment variable

set -e

# Route to console CLI if MODE is "console", otherwise start API server
if [ "$MODE" = "console" ]; then
    exec python3 -m ATA.main
elif [ "$MODE" = "api" ]; then
    exec uvicorn ATA.server:app --host 0.0.0.0 --port 8000
else
    exec uvicorn ATA.server:app --host 0.0.0.0 --port 8000
fi


