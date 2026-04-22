FROM python:3.11-slim

# Ish papkasi
WORKDIR /app

# Tizim paketlarini yangilash
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Dependency'larni avval o'rnatish (cache uchun)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini ko'chirish
COPY . .

# Database papkasini yaratish
RUN mkdir -p /app/data

# Database faylini saqlash uchun volume
VOLUME ["/app/data"]

# Muhit o'zgaruvchilari
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DATABASE_PATH=data/kimyo_bot.db

# Botni ishga tushirish
CMD ["python", "main.py"]
