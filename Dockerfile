# Use an official Python runtime as a parent image
FROM python:3.14-slim

# Set a default port. This can be overridden at runtime, e.g., docker run -e PORT=8080
ENV PORT=80

# Set the working directory
WORKDIR /app

# Create a non-root user for security and switch to it
RUN useradd -m appuser
USER appuser

# Add user's local bin to PATH to find installed packages like uvicorn
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy requirements first to leverage Docker layer caching
COPY --chown=appuser:appuser requirements.txt .

# Install dependencies as the non-root user
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy the rest of the application code
COPY --chown=appuser:appuser . .

# Expose the default port. The actual port used is determined by the PORT env var.
EXPOSE 80

# Use a shell to launch so we can substitute the PORT environment variable.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
