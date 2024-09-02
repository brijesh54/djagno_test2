# DJTest Django App

This project is a Django application named `djtest`. The application has been containerized using Docker for easier deployment and development. This README provides instructions on how to build and run the Docker container.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose (if you plan to use it): [Install Docker Compose](https://docs.docker.com/compose/install/)

## Docker Setup

### 1. Dockerfile

A `Dockerfile` is included in the project root directory. This file contains the instructions to build a Docker image for the Django app.

### 2. .dockerignore

A `.dockerignore` file is also included to exclude unnecessary files from the Docker image, such as `.pyc` files and local environment variables.

## Build and Run the Docker Container

### Using Docker Only

1. **Build the Docker image:**

   ```bash
   docker build -t djtest .

2. **RUN Docker image Build:**

   ```bash
   docker run -p 8000:8000 djtest



