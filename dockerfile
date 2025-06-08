# Use the newer, specific base image (Your suggestion)
FROM python:3.13-slim-bookworm

# Add OS-level updates and security hardening (Your suggestion)
RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    pip install --no-cache-dir --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

# Set Python environment variables for container best practices (Your suggestion)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy and install Python dependencies (this order is efficient for Docker's cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot script into the container
COPY bot.py .

# This is the command that will run when the container starts
CMD ["python3", "bot.py"]