#!/bin/bash

# Start the backend server
echo "Starting backend server..."
cd social-media-manager-app
python3 app.py &
BACKEND_PID=$!
cd ..

# Start the frontend server
echo "Starting frontend server..."
cd social-media-manager-frontend
npm run dev &
FRONTEND_PID=$!

# Wait for both processes to exit
wait $BACKEND_PID
wait $FRONTEND_PID
