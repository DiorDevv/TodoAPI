# 📦 TodoAPI — Django DRF + Docker + CI/CD

Bu loyiha Docker va CI/CD ni amaliy o'rganish uchun yaratilgan.

## 🏗️ Texnologiyalar

| Texnologiya | Vazifasi |
|---|---|
| Django 5 + DRF | Backend API |
| PostgreSQL | Asosiy baza |
| Redis | Cache |
| Nginx | Reverse proxy |
| Docker + Compose | Konteynerlashtirish |
| GitHub Actions | CI/CD pipeline |

---

## 🚀 Ishga tushirish

### 1. Klonlash

```bash
git clone https://github.com/DiorDevv/TodoAPI.git
cd todoapi
```

### 2. Environment variables

```bash
cp .env.example .env
# .env faylini tahrirlang
```

### 3. Docker bilan ishga tushirish

```bash
# Barcha servicelarni build va start
docker compose up -d

# Loglarni kuzatish
docker compose logs -f web

# API tekshirish
curl http://localhost/api/todos/
```

### 4. Foydalanuvchi yaratish

```bash
docker compose exec web python manage.py createsuperuser
```

---

## 🔌 API Endpoints

### Autentifikatsiya

```
POST /api/auth/register/   - Ro'yxatdan o'tish
GET  /api/auth/me/         - Profil
GET  /api/auth/login/      - Login (DRF browsable)
```

### Todolar (autentifikatsiya kerak)

```
GET    /api/todos/              - Ro'yxat (filter, search, sort)
POST   /api/todos/              - Yangi yaratish
GET    /api/todos/{id}/         - Bitta olish
PUT    /api/todos/{id}/         - To'liq yangilash
PATCH  /api/todos/{id}/         - Qisman yangilash
DELETE /api/todos/{id}/         - O'chirish
POST   /api/todos/{id}/toggle/  - Bajarildi/emas almashtirish
```

### Filterlash

```
GET /api/todos/?is_completed=true
GET /api/todos/?priority=high
GET /api/todos/?search=Python
GET /api/todos/?ordering=-created_at
```

---

## 🐳 Docker tushunchasi

```
                  ┌─────────────────────────────┐
Internet ──►  :80 │  nginx (Reverse Proxy)       │
                  │  /static/ → disk             │
                  │  /        → web:8000         │
                  └─────────────┬───────────────┘
                                │
                  ┌─────────────▼───────────────┐
                  │  web (Django + Gunicorn)     │
                  │  :8000 (ichki)               │
                  └──────┬──────────┬────────────┘
                         │          │
               ┌─────────▼──┐  ┌───▼──────┐
               │ db          │  │ redis    │
               │ PostgreSQL  │  │ Cache    │
               │ :5432       │  │ :6379    │
               └─────────────┘  └──────────┘
```

### Foydali buyruqlar

```bash
# Container ichiga kirish
docker compose exec web bash
docker compose exec db psql -U postgres todoapp

# Migratsiya qo'lda
docker compose exec web python manage.py migrate

# Testlarni ishlatish
docker compose exec web python manage.py test

# Image qayta build
docker compose build web
docker compose up -d web
```

---

## ⚙️ CI/CD Pipeline

```
git push → GitHub → Actions trigger

  CI (barcha push/PR):
  ├── 1. Python + dependencies o'rnatish
  ├── 2. flake8 linting
  ├── 3. black format tekshirish
  └── 4. pytest testlar (postgres service bilan)

  CD (faqat main branch):
  ├── 1. Docker image build (multi-stage)
  ├── 2. Docker Hub ga push (:latest + :sha)
  ├── 3. SSH orqali serverga kirish
  ├── 4. Migratsiya ishlatish
  └── 5. docker compose up -d --no-deps web
```

### GitHub Secrets sozlash

`Settings > Secrets and variables > Actions` ga qo'shing:

| Secret | Qiymati |
|---|---|
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_TOKEN` | Docker Hub access token |
| `SSH_HOST` | Server IP manzili |
| `SSH_USER` | SSH foydalanuvchi |
| `SSH_PRIVATE_KEY` | SSH private key |

---

## 📁 Loyiha tuzilmasi

```
todoapi/
├── .github/
│   └── workflows/
│       └── ci-cd.yml       ← CI/CD pipeline
├── app/
│   ├── api/
│   │   ├── models.py       ← Todo modeli
│   │   ├── serializers.py  ← DRF serializers
│   │   ├── views.py        ← ViewSet va views
│   │   └── tests.py        ← Testlar
│   └── core/
│       ├── settings.py     ← Django sozlamalari
│       └── urls.py         ← URL routing
├── nginx/
│   └── nginx.conf          ← Nginx konfiguratsiya
├── Dockerfile              ← Multi-stage build
├── docker-compose.yml      ← Barcha servicelar
├── requirements.txt
├── .env.example
└── README.md
```
