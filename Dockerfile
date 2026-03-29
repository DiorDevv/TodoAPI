# =============================================================
# DOCKERFILE - Multi-stage build
# =============================================================
# Stage 1 (builder): kutubxonalarni compile qiladi
# Stage 2 (production): faqat kerakli narsalar - kichik image
# =============================================================

# ---- Stage 1: Builder ----
FROM python:3.12-slim AS builder

# Python cache fayllarini yaratmaslik
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies (psycopg2 uchun)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Kutubxonalarni virtual muhitga o'rnatish
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# requirements ni AVVAL ko'chirish (Docker cache dan foydalanish)
# Agar requirements.txt o'zgarmasa, bu qadam cache dan keladi
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ---- Stage 2: Production ----
FROM python:3.12-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Runtime uchun faqat libpq kerak (gcc emas)
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Builder stage dan virtual env ni olish
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Root bo'lmagan foydalanuvchi (xavfsizlik uchun)
RUN addgroup --system appgroup && adduser --system --group appuser

# Loyiha kodini ko'chirish
COPY . .

# Static fayllarni yig'ish
RUN python manage.py collectstatic --noinput

# Fayllar egasini o'zgartirish
RUN chown -R appuser:appgroup /app

USER appuser

# Port ochish (faqat hujjat uchun, docker-compose da belgilanadi)
EXPOSE 8000

# Ishga tushirish buyrug'i
# gunicorn - production WSGI server
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "120", \
     "app.core.wsgi:application"]
