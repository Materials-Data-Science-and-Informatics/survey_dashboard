# Multi-stage build for survey dashboard
# Stage 1: Builder - installs dependencies
FROM python:3.12-slim as builder

# Install poetry
RUN pip install --no-cache-dir poetry==1.8.2

WORKDIR /app

# Copy dependency files first (for Docker layer caching)
COPY pyproject.toml poetry.lock README.md ./

# Configure poetry to not create virtual environment (we're in a container)
RUN poetry config virtualenvs.create false

# Install dependencies (excluding dev dependencies)
# --no-root: Don't install the project itself, only dependencies
RUN poetry install --only main --no-root --no-interaction --no-ansi

# Stage 2: Final runtime image
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY survey_dashboard/ ./survey_dashboard/
COPY pyproject.toml ./

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose the application port
EXPOSE 5006

# Run the application in production mode using the updated script
CMD ["survey-dashboard", "--production", "--host", "0.0.0.0", "--port", "5006"]
