# ╔══════════════════════════════════════════════════════════════╗
# ║         CHEVROLET UZ — DJANGO LOYIHASI                       ║
# ║         Ustoz uchun to'liq qo'llanma                         ║
# ╚══════════════════════════════════════════════════════════════╝
#
# TALABA: [Ismingizni shu yerga yozing]
# LOYIHA: Chevrolet.uz saytining Django kloni
# TEXNOLOGIYALAR: Python 3.11+, Django 5.x, Bootstrap 5, SQLite
# ================================================================

═══════════════════════════════════════════════════════════════════
  LOYIHA TUZILISHI VA HAR BIR FAYLNING VAZIFASI
═══════════════════════════════════════════════════════════════════

chevrolet_uz/                        ← Asosiy loyiha papkasi
│
├── manage.py                        ← Django buyruqlarini ishga tushirish uchun
│
├── requirements.txt                 ← Kerakli Python kutubxonalar ro'yxati
│
├── .env.example                     ← Maxfiy sozlamalar namunasi
│
├── chevrolet_uz/                    ← Loyiha sozlamalari papkasi
│   ├── settings.py                  ← BARCHA sozlamalar (DB, media, xavfsizlik)
│   ├── urls.py                      ← BOSH URL marshrutlagich
│   └── wsgi.py                      ← Production server uchun
│
├── main/                            ← Asosiy ilova (barcha mantiq shu yerda)
│   ├── models.py                    ← MA'LUMOTLAR BAZASI MODELLARI (7 ta jadval)
│   ├── admin.py                     ← ADMIN PANEL sozlamalari
│   ├── views.py                     ← SAHIFALAR MANTIQI (qanday ishlasin)
│   ├── forms.py                     ← FORMALAR (ro'yxatdan o'tish, profil)
│   ├── urls.py                      ← ILOVA URL yo'llari
│   ├── signals.py                   ← AVTOMATIK ishlar (profil yaratish)
│   ├── apps.py                      ← Ilova konfiguratsiyasi
│   ├── templatetags/
│   │   └── url_tags.py              ← Shablon yordamchi funksiyasi
│   ├── fixtures/
│   │   └── initial_data.json        ← Demo ma'lumotlar (3 mashina, 2 yangilik)
│   └── migrations/                  ← Ma'lumotlar bazasi o'zgarishlari tarixi
│
├── templates/                       ← HTML shablonlar
│   ├── base.html                    ← ASOSIY SHABLON (navbar + footer)
│   ├── registration/
│   │   ├── login.html               ← Kirish sahifasi
│   │   └── register.html           ← Ro'yxatdan o'tish sahifasi
│   └── main/
│       ├── index.html               ← BOSH SAHIFA (banner + mashinalar)
│       ├── car_list.html            ← Mashinalar ro'yxati (filterlar bilan)
│       ├── car_detail.html          ← Bitta mashina batafsil sahifasi
│       ├── news_list.html           ← Yangiliklar ro'yxati
│       ├── news_detail.html         ← Bitta yangilik batafsil
│       └── profile.html            ← Foydalanuvchi profili
│
├── static/
│   └── images/
│       └── default-avatar.svg      ← Standart profil rasmi
│
└── media/                          ← Foydalanuvchilar yuklagan fayllar (auto)


═══════════════════════════════════════════════════════════════════
  ISHGA TUSHIRISH — QADAMMA-QADAM
═══════════════════════════════════════════════════════════════════

1-QADAM: Virtual muhit yaratish
────────────────────────────────
  Windows (PowerShell):
    python -m venv venv
    venv\Scripts\activate

  Mac / Linux (Terminal):
    python3 -m venv venv
    source venv/bin/activate

  ✅ Muvaffaqiyat belgisi: (venv) so'z chap tomonda ko'rinadi

2-QADAM: Paketlarni o'rnatish
──────────────────────────────
    pip install -r requirements.txt

  ✅ Muvaffaqiyat belgisi: "Successfully installed django..." xabari

3-QADAM: Ma'lumotlar bazasini tayyorlash
──────────────────────────────────────────
    python manage.py makemigrations
    python manage.py migrate

  ✅ Muvaffaqiyat belgisi: "OK" so'zi har qatorda ko'rinadi

4-QADAM: Demo ma'lumotlarni yuklash
─────────────────────────────────────
    python manage.py loaddata main/fixtures/initial_data.json

  ✅ Muvaffaqiyat belgisi: "Installed 12 object(s)" xabari

5-QADAM: Admin foydalanuvchi yaratish
──────────────────────────────────────
    python manage.py createsuperuser

  So'raydi:
    Username: admin (yoki o'zingiz xohlagan)
    Email: admin@example.com
    Password: (kamida 8 belgi, ko'rinmaydi — bu normal)
    Password (again): (qayta kiriting)

  ✅ Muvaffaqiyat belgisi: "Superuser created successfully."

6-QADAM: Serverni ishga tushirish
───────────────────────────────────
    python manage.py runserver

  ✅ Muvaffaqiyat belgisi:
    Starting development server at http://127.0.0.1:8000/


═══════════════════════════════════════════════════════════════════
  SAYTNI OCHISH
═══════════════════════════════════════════════════════════════════

  Brauzerda oching:

  🌐 Asosiy sayt:    http://127.0.0.1:8000/
  🔐 Admin panel:    http://127.0.0.1:8000/admin/
  👤 Kirish:         http://127.0.0.1:8000/login/
  📝 Ro'yxat:        http://127.0.0.1:8000/register/
  🚗 Mashinalar:     http://127.0.0.1:8000/cars/
  📰 Yangiliklar:    http://127.0.0.1:8000/news/


═══════════════════════════════════════════════════════════════════
  ADMIN PANELDA NIMA QILISH MUMKIN
═══════════════════════════════════════════════════════════════════

  http://127.0.0.1:8000/admin/ ga kiring (admin/parol bilan)

  1. HERO BANNERLAR qo'shish:
     Admin → Hero Bannerlar → + Qo'shish
     → Rasm yuklang (1920×900 px tavsiya etiladi)
     → Sarlavha yozing
     → Tartib raqami bering (1, 2, 3...)
     → Faol: ✓ belgilang
     → Saqlang

  2. MASHINA qo'shish:
     Admin → Avtomobillar → + Qo'shish
     → Barcha maydonlarni to'ldiring
     → "Rasmlar" bo'limida rasm yuklang (asosiy rasmni belgilang)
     → Saqlang

  3. YANGILIK qo'shish:
     Admin → Yangiliklar → + Qo'shish
     → Sarlavha, matn yozing
     → Muqova rasmi yuklang
     → "Nashr etilgan" belgilang
     → Saqlang

  4. FOYDALANUVCHI ko'rish:
     Admin → Foydalanuvchilar → (ro'yxatdan o'tganlar ko'rinadi)


═══════════════════════════════════════════════════════════════════
  LOYIHANING ASOSIY FUNKSIYALARI
═══════════════════════════════════════════════════════════════════

  ✅ RO'YXATDAN O'TISH — /register/
     Ism, familiya, email, parol bilan ro'yxatdan o'tish
     Xatolar chiroyli ko'rsatiladi

  ✅ KIRISH — /login/
     Username va parol bilan kirish
     "Parolni ko'rsatish" tugmasi mavjud

  ✅ HERO BANNER — bosh sahifada
     Admin orqali rasm yuklash mumkin
     Bir nechta banner = avtomatik slayder

  ✅ MASHINALAR — /cars/
     Brend, kategoriya, narx bo'yicha filter
     Qidiruv qutisi
     Sahifalash (12 tadan)

  ✅ MASHINA BATAFSIL — /cars/tracker-2024/
     Rasm galereyasi (thumbnail lenta)
     Texnik xarakteristikalar accordion
     Ko'rishlar soni oshadi

  ✅ PROFIL — /profile/
     Faqat kirgan foydalanuvchi ko'ra oladi
     Avatar yuklash (400×400 ga avtomatik kesish)
     Ma'lumotlarni tahrirlash

  ✅ ADMIN PANEL — /admin/
     Rasm thumbnail preview
     Qidiruv va filterlar
     Inline galereya qo'shish


═══════════════════════════════════════════════════════════════════
  UMUMIY XATOLAR VA YECHIMLARI
═══════════════════════════════════════════════════════════════════

  ❌ "No module named django"
  ✅ Yechim: pip install -r requirements.txt (virtual muhit faol bo'lsin)

  ❌ "Table doesn't exist"
  ✅ Yechim: python manage.py migrate

  ❌ "FileNotFoundError: logs/"
  ✅ Yechim: settings.py da logs papkasi avtomatik yaratiladi (mkdir)

  ❌ Media rasmlar ko'rinmayapti
  ✅ Yechim: settings.py da DEBUG=True bo'lishi kerak

  ❌ "CSRF token missing"
  ✅ Yechim: Barcha formalarda {% csrf_token %} mavjud (allaqachon qo'yilgan)


═══════════════════════════════════════════════════════════════════
  TEXNIK MA'LUMOTLAR (IMTIHON UCHUN)
═══════════════════════════════════════════════════════════════════

  Framework:    Django 5.0.6
  Til:          Python 3.11+
  Frontend:     Bootstrap 5.3 + custom CSS
  Ma'lumotlar:  SQLite (development), PostgreSQL (production)
  Rasm:         Pillow — avtomatik optimallashtirish
  Arxitektura:  MVT (Model-View-Template)

  XAVFSIZLIK:
  • CSRF himoya — barcha formalarda token
  • LoginRequiredMixin — profil sahifasi himoyalangan
  • Parol validatsiyasi — 8 belgidan kam bo'lmaydi
  • XSS himoya — Django template auto-escape
  • Media validatsiya — fayl turi va hajmi tekshiriladi

  MODELLAR (ma'lumotlar bazasi jadvallari):
  • CarBrand     — Avtomobil brendlari
  • CarCategory  — Kategoriyalar (Sedan, SUV...)
  • Car          — Asosiy mashina (20+ maydon)
  • CarImage     — Galereya rasmlari (ko'p-ko'p)
  • NewsCategory — Yangilik kategoriyalari
  • News         — Yangiliklar
  • UserProfile  — Foydalanuvchi profili (OneToOne)
  • HeroBanner   — Bosh sahifa bannerlari

  VIEWS (ko'rinishlar):
  • RegisterView  — Ro'yxatdan o'tish (GET+POST)
  • HomeView      — Bosh sahifa (TemplateView)
  • CarListView   — Ro'yxat (ListView + filter)
  • CarDetailView — Batafsil (DetailView + slug)
  • NewsListView  — Yangiliklar ro'yxati
  • NewsDetailView— Yangilik batafsil
  • ProfileView   — Profil (LoginRequiredMixin)
  • SearchView    — Global qidiruv

