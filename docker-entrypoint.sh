#!/bin/bash
set -e

if [ "$MODE" = "console" ]; then
    exec python3 -m ATA.main
elif [ "$MODE" = "api" ]; then
    exec uvicorn ATA.server:app --host 0.0.0.0 --port 8000
else
    exec uvicorn ATA.server:app --host 0.0.0.0 --port 8000
fi


