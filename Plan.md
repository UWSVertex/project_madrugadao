# Car Sales Website — Project Plan

**Stack:** Django (backend) + Bootstrap/HTML/CSS (frontend, server-rendered templates)
**Env:** Anaconda virtual environment `djangoDev` — activate with `conda activate djangoDev`
**Reference site:** https://webautosmyr1.onrender.com (Autos MYR — used car dealer in San Sebastián, Costa Rica)
**Project layout (already scaffolded):**
- Project: `mrcards/` (settings, urls, wsgi, asgi)
- App: `carlisting/` (models, views, admin — currently empty)

Check off each item as it is completed.

---

## Phase 0 — Environment & Project Setup
- [x] Confirm `djangoDev` conda env has Django 6.0.8, Pillow installed (verified: yes)
- [ ] Add `crispy-forms` / `crispy-bootstrap5` (optional, for nicer admin-facing forms) or skip and use plain Bootstrap forms
- [x] Create `requirements.txt` (django, pillow, gunicorn, whitenoise, python-dotenv, dj-database-url) for Render deployment
- [x] Add `carlisting` to `INSTALLED_APPS` in `mrcards/settings.py`
- [x] Configure `TEMPLATES['DIRS']` to project-level `templates/` folder
- [x] Configure `STATICFILES_DIRS` for project-level `static/` folder (css/js/images)
- [x] Configure `MEDIA_URL` / `MEDIA_ROOT` for uploaded car images
- [x] Set up `.env` handling for `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` (python-dotenv)
- [x] Initialize git repository, add `.gitignore` (venv, __pycache__, db.sqlite3, .env, media/)

## Phase 1 — Data Models (`carlisting/models.py`)
- [x] `CarBrand` model (name, logo)
- [x] `CarListing` model: brand (FK), model_name, year, price, mileage, fuel_type, transmission, body_type, color, description, is_available/is_sold, is_featured, created_at, updated_at
- [x] `CarImage` model (FK to CarListing, image, is_primary) — supports multiple photos per listing
- [x] `Inquiry`/`ContactMessage` model (name, phone, email, message, related car FK optional, created_at) for customer contact form
- [x] Run `makemigrations` and `migrate`
- [x] Register models in `carlisting/admin.py` with `ModelAdmin` (list_display, search_fields, list_filter, inline `CarImage` admin)
- [x] Create Django superuser for admin access

## Phase 2 — Admin Customization
- [x] Customize Django admin site header/title ("Car Sales Admin")
- [x] Add image preview thumbnails in admin list/detail view
- [x] Add inline image upload (multiple images per car) via `TabularInline`/`StackedInline`
- [x] Add filters: brand, availability, featured, price range, year
- [x] Restrict admin access to staff/superuser accounts only (default Django behavior — verify)
- [x] Test: log in to `/admin/`, add a new car listing with images, edit, mark as sold/delete

## Phase 3 — Public Frontend (Views + Templates + Bootstrap)
- [x] Add Bootstrap 5 (via CDN or local static files) + base template with navbar/footer
- [x] `base.html` — shared layout (navbar, footer, meta tags, Bootstrap/CSS links)
- [x] Home page view — hero banner, featured listings, dealership info (mirroring reference site)
- [x] Car listing (inventory) page — grid of cards (image, price, year, mileage), pagination
- [x] Car detail page — image gallery/carousel, full specs, contact/inquiry button
- [x] Search & filter UI (by brand, price range, year, body type)
- [x] Contact page — dealership address/phone/hours, contact form (saves to `Inquiry` model)
- [ ] About page (optional, dealership info)
- [x] Wire up `urls.py` for `mrcards` (project) and `carlisting` (app, via `include()`)
- [ ] Custom 404/500 error templates styled with Bootstrap

## Phase 4 — Styling & Static Assets
- [x] Add custom `static/css/style.css` for branding colors/fonts (match dealership branding)
- [ ] Add logo/favicon
- [ ] Make pages responsive (test mobile/tablet/desktop breakpoints)
- [ ] Add placeholder/default image for cars without photos

## Phase 5 — Forms & Validation
- [x] Contact/inquiry form using Django `ModelForm` with CSRF protection
- [ ] Client-side validation (Bootstrap validation classes) + server-side validation
- [x] Success/error messages via Django `messages` framework

## Phase 6 — Testing
- [ ] Write model tests (`carlisting/tests.py`) — CarListing, CarImage creation
- [ ] Write view tests — inventory list, detail page, contact form submission
- [ ] Manually test full admin workflow: add/edit/delete listing with images
- [ ] Manually test full public flow: browse, filter, view detail, submit inquiry
- [x] Run `python manage.py check` and fix warnings

## Phase 7 — Deployment (Render, matching reference site)
- [x] Add `gunicorn` + `whitenoise` for static file serving in production
- [ ] Configure `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` for `.onrender.com` domain
- [ ] Set `DEBUG=False` and secure `SECRET_KEY` via environment variable
- [ ] Add `render.yaml` or configure Render web service (build/start commands)
- [ ] Configure persistent/production database if needed (Render Postgres) or keep SQLite for MVP
- [ ] Set up media file storage strategy (Render disk or external storage, since SQLite/local media is ephemeral on free tier)
- [ ] Deploy and verify live site + `/admin/` login works
- [ ] Create production superuser on deployed instance

## Phase 8 — Polish & Launch
- [ ] SEO basics: meta tags, page titles, descriptions (mirroring reference site's approach)
- [ ] Add Google Maps embed / dealership location (optional)
- [ ] Final content review (real car listings, prices, images)
- [ ] Final QA pass on all pages/devices
- [ ] Launch 🎉
