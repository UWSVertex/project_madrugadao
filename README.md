# Car Sales Website (Django)

A car dealership website with a public inventory browsing frontend (Bootstrap 5)
and a Django admin backend for staff to manage car listings, images, and customer
inquiries.

## Local Development

```bash
conda activate djangoDev
cp .env.example .env          # first time only
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000/ for the public site and http://127.0.0.1:8000/admin/
to manage listings.

## Deploying to Render

This repo is set up for a **Render Web Service** (Python) with an optional
managed **PostgreSQL** database.

### Option A — Blueprint (`render.yaml`)
1. Push this repo to GitHub.
2. In the Render dashboard, choose **New > Blueprint** and point it at the repo.
   Render will read [render.yaml](./render.yaml) and provision both the web
   service and the free Postgres database automatically.
3. After the first deploy, open the service **Shell** tab and run:
   ```bash
   python manage.py createsuperuser
   ```

### Option B — Manual Web Service
1. **New > Web Service**, connect the repo.
2. Runtime: `Python 3`.
3. Build Command: `./build.sh`
4. Start Command: `gunicorn mrcards.wsgi:application --bind 0.0.0.0:$PORT`
5. Add environment variables:
   | Key | Value |
   |---|---|
   | `SECRET_KEY` | (generate a random string) |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `your-app-name.onrender.com` |
   | `CSRF_TRUSTED_ORIGINS` | `https://your-app-name.onrender.com` |
   | `DATABASE_URL` | (from a Render Postgres instance, or omit to use SQLite) |
6. Deploy, then use the **Shell** tab to run `python manage.py createsuperuser`.

### Notes
- Static files are served in production via **WhiteNoise** — `build.sh` runs
  `collectstatic` automatically on every deploy.
- **Media files** (car photos uploaded via the admin) are stored on local disk
  by default, which is **ephemeral on Render's free tier** (files are lost on
  redeploy/restart). For a production launch, either:
  - Add a [Render Disk](https://render.com/docs/disks) mounted at `MEDIA_ROOT`, or
  - Switch to an external storage backend (e.g. `django-storages` + S3/Cloudinary).
- SQLite works for a quick demo, but Postgres (via `DATABASE_URL`) is
  recommended for anything persistent — data on the free web service's local
  disk does not survive redeploys.
