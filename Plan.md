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
- [x] Create `requirements.txt` (django, pillow, python-dotenv) for local development
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

## Phase 7 — Deployment
- [x] Not deploying to Render — this project runs locally only (reference site was used for design inspiration, not as a deployment target)

## Phase 8 — Polish & Launch
- [ ] SEO basics: meta tags, page titles, descriptions (mirroring reference site's approach)
- [ ] Add Google Maps embed / dealership location (optional)
- [ ] Final content review (real car listings, prices, images)
- [ ] Final QA pass on all pages/devices
- [ ] Launch 🎉

## Phase 9 — Custom Staff Administration Panel
A fully custom, branded staff dashboard at `/panel/` (separate from Django's
built-in `/admin/`, which still exists and works but isn't linked publicly).
- [x] `carlisting/forms.py` — `CarBrandForm`, `CarListingForm`, `CarImageForm`,
      `CarImageFormSet` (inline formset, extra=3, can_delete=True, multi-photo upload)
- [x] `carlisting/panel_urls.py` (`app_name='panel'`) — login, logout, dashboard,
      cars (list/new/edit/delete), brands (list/delete), inquiries (list/toggle)
- [x] Panel views in `carlisting/views.py`, all gated with
      `@login_required(login_url='panel:login')` + `@user_passes_test(is_staff_user)`
- [x] `LOGIN_URL` / `LOGIN_REDIRECT_URL` / `LOGOUT_REDIRECT_URL` configured in settings
- [x] `templates/panel/` — `base.html` (sidebar layout), `login.html`, `dashboard.html`,
      `car_list.html`, `car_form.html` (multi-image upload), `car_confirm_delete.html`,
      `brand_list.html`, `inquiry_list.html`
- [x] `static/css/panel.css` — dark sidebar, stat cards, table cards, login card,
      styled to visually match the public site's branding
- [x] "Panel" link intentionally **not** shown in the public navbar (security —
      staff must navigate to `/panel/login/` directly)
- [x] Verified end-to-end: login → add brand → add car listing with photo upload →
      appears correctly on public inventory page → edit/delete → dashboard stats update
- [x] Local dev superuser: username `admin` / password `admin12345`
      (⚠️ change before any real/production use — `python manage.py changepassword admin`)

## Phase 10 — Design Iterations & Branding Updates
Ongoing refinements made after the initial Autos MYR redesign, based on user feedback.
- [x] Removed all Render deployment leftovers (`build.sh`, `Procfile`, `render.yaml`,
      whitenoise/gunicorn/dj-database-url/psycopg2 deps, production security block) —
      project intentionally runs locally only
- [x] Added Facebook / Instagram / TikTok social icons to the topbar and footer
      (`.topbar__social`, `.footer-social` in `static/css/style.css`)
- [x] Fixed the home page hero search card — originally used a negative-margin
      "floating card" overlap trick that clipped/was covered by the section below;
      redesigned so the search card sits fully inside the dark hero section with its
      own padding, and the next section starts cleanly with normal spacing
- [x] Replaced the "Conocer Autos MYR" about/feature-list section on the home page
      with a simple contact form (name, phone, email, message) that reuses the
      existing `InquiryForm`/`Inquiry` model — submissions appear in the panel's
      "Consultas" list alongside per-car inquiries
- [x] **Rebranded accent color** from yellow (`#F9EE08`) to sage green **`#7E9867`**
      (RGB 126, 152, 103) across the entire site and panel:
      - Renamed CSS variable `--myr-yellow` → `--myr-accent` in `static/css/style.css`
        and `static/css/panel.css`
      - Renamed `.btn-myr-yellow` → `.btn-myr-accent` across all templates
      - Added `.text-myr-accent` utility class, replacing Bootstrap's `text-warning`
        usages on the home page (feature icons, footer column labels) so the accent
        matches exactly instead of relying on Bootstrap's default amber
      - Adjusted derived shades for contrast/hover states: darker hover green
        (`#6c8558`), dark-green text-on-white for `.section-eyebrow` (`#5E724D`),
        dark-green icon fill for `.feature-icon`/`.stat-icon` (`#445539` on a
        `rgba(126, 152, 103, …)` tint background)
      - Updated `<meta name="theme-color">` in `templates/base.html`
      - Verified visually across home page (hero, CTA band, footer, buttons) and
        the staff panel (login button, active sidebar nav, stat card icons)
