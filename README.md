# 🧪 Kimyo Bot

Kimyo fanidan resurslar, testlar va foydali materiallarni boshqarish uchun Telegram bot.

## Xususiyatlari

- 📂 Resurslarni boshqarish (PDF, video, havolalar)
- 📝 Test/quiz tizimi
- 🔍 Qidirish
- ⭐ Sevimlilar
- 🏆 Reyting tizimi
- 📢 Broadcast xabarlar
- 📊 Statistika va eksport (CSV/Excel)
- 💬 Fikr bildirish
- 💡 Kunlik kimyo maslahatlari
- ⏰ Avtomatik kunlik maslahat (har kuni 09:00)

## O'rnatish

### 1. Loyihani serverga ko'chirish

```bash
git clone <repo-url> kimyo-bot
cd kimyo-bot
```

### 2. Virtual muhit yaratish

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Paketlarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. .env faylni sozlash

```bash
cp .env.example .env
nano .env
```

`.env` faylga quyidagilarni kiriting:
```
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id_here
```

- `BOT_TOKEN` — @BotFather dan olingan token
- `ADMIN_ID` — Admin Telegram ID raqami

### 5. Botni ishga tushirish

```bash
python main.py
```

## Serverda doimiy ishga tushirish (systemd)

```bash
sudo nano /etc/systemd/system/kimyo-bot.service
```

Quyidagini kiriting:
```ini
[Unit]
Description=Kimyo Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/kimyo-bot
ExecStart=/root/kimyo-bot/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Keyin:
```bash
sudo systemctl daemon-reload
sudo systemctl enable kimyo-bot
sudo systemctl start kimyo-bot
```

Loglarni ko'rish:
```bash
sudo journalctl -u kimyo-bot -f
```

## Loyiha tuzilishi

```
kimyo-bot/
├── main.py              # Asosiy ishga tushirish fayli
├── requirements.txt     # Python paketlari
├── .env                 # Sozlamalar (token, admin ID)
├── .env.example         # Sozlamalar namunasi
├── run.sh               # Ishga tushirish skripti
└── app/
    ├── config.py        # Konfiguratsiya
    ├── database/
    │   ├── engine.py    # Database ulanishi
    │   ├── models.py    # Jadval modellari
    │   └── queries.py   # Database so'rovlari
    ├── filters/
    │   └── admin.py     # Admin filtri
    ├── handlers/
    │   ├── start.py     # /start va ro'yxatdan o'tish
    │   ├── menu.py      # Asosiy menyu va /admin
    │   ├── resources.py # Resurslarni ko'rish
    │   ├── quiz.py      # Test yechish
    │   ├── favorites.py # Sevimlilar
    │   ├── feedback.py  # Fikr bildirish
    │   ├── admin_resources.py  # Admin: resurslar
    │   ├── admin_quiz.py       # Admin: testlar
    │   ├── admin_broadcast.py  # Admin: xabar yuborish
    │   ├── admin_stats.py      # Admin: statistika
    │   └── admin_feedback.py   # Admin: fikrlar
    ├── keyboards/
    │   ├── inline.py    # Inline tugmalar
    │   └── reply.py     # Reply tugmalar
    ├── middlewares/
    │   └── db.py        # Database middleware
    ├── services/
    │   └── scheduler.py # Kunlik maslahat scheduler
    ├── states/
    │   ├── registration.py
    │   ├── resource.py
    │   ├── quiz.py
    │   ├── search.py
    │   ├── broadcast.py
    │   └── feedback.py
    └── utils/
        └── texts.py     # Barcha matnlar (o'zbek tilida)
```
