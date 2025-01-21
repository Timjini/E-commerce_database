#!/bin/bash
if [ -f "/app/app/app.py" ]; then
    python /app/app/app.py
else
    echo "Error: app.py not found!"
    exit 1
fi
