#!/bin/bash
# Kimyo Bot - Ishga tushirish skripti

# Virtual muhitni faollashtirish (agar mavjud bo'lsa)
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# .env faylni tekshirish
if [ ! -f ".env" ]; then
    echo "❌ .env fayl topilmadi!"
    echo "📋 .env.example dan nusxa olib, sozlang:"
    echo "   cp .env.example .env"
    exit 1
fi

# Kerakli paketlarni o'rnatish
echo "📦 Paketlarni tekshirilmoqda..."
pip install -r requirements.txt --quiet

# Botni ishga tushirish
echo "🚀 Kimyo Bot ishga tushmoqda..."
python main.py
