# Stage 1: Build & Install dependencies
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim AS runtime
WORKDIR /app
COPY --from=builder /install /usr/local

# HANYA PERLU COPY ./app karena di dalamnya sudah mencakup models/ dan data/
COPY ./app ./app

# Jalankan sebagai user biasa untuk keamanan
RUN adduser --disabled-password appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]