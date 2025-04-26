# Frontend build
FROM node:22 as build

# Set working directory
WORKDIR /workspace/frontend

# Copy package files
COPY ./frontend/package.json ./

# Install dependencies
RUN npm install --force

ENV SHELL=/bin/bash

# Copy all files and dirs in frontend
COPY ./frontend ./

# Serve the app
RUN npm install --save-dev serve

# Build the application
RUN npm run build

# Start dev server
CMD ["serve", "-s", "frontend/build"]

# Backend build
FROM python:3.12

# Set environment time zone
ENV TZ="America/New_York"

# Install latest version of pip
RUN python3 -m pip install --upgrade pip

# Copy requirements and install dependencies
COPY ./backend/requirements.txt /workspace/backend/requirements.txt

# Install backend dependencies
RUN pip install --no-cache-dir --upgrade -r /workspace/backend/requirements.txt

# Copy all other backend resources
COPY --from=build /workspace/static /workspace/static
COPY ./backend /workspace/backend
COPY ./alembic.ini /workspace/alembic.ini

WORKDIR /workspace
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]

EXPOSE 8080