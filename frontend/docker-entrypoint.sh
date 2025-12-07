#!/bin/sh
# Docker entrypoint script for frontend
# Injects environment variables into React build

# Replace environment variables in JavaScript files
if [ -n "$REACT_APP_BACKEND_URL" ]; then
    echo "Configuring backend URL: $REACT_APP_BACKEND_URL"
    find /usr/share/nginx/html -type f -name "*.js" -exec sed -i "s|REACT_APP_BACKEND_URL_PLACEHOLDER|$REACT_APP_BACKEND_URL|g" {} +
fi

# Start nginx
exec "$@"
