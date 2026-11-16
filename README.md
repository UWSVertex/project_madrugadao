# Car Sales Website (Django)

A car dealership website with a public inventory browsing frontend (Bootstrap 5)
and a Django admin backend for staff to manage car listings, images, and customer
inquiries.

## Run with Docker

Requires Docker with the Compose plugin.

```bash
cp .env.example .env          # first time only
docker compose up --build
```

Visit http://127.0.0.1:1414/ for the public site, http://127.0.0.1:1414/admin/
for the Django admin, and http://127.0.0.1:1414/panel/ for the staff panel.
The project directory is mounted into the container, so SQLite data and uploaded
media persist on the host. Create a staff account with:

```bash
docker compose exec web python manage.py createsuperuser
```

Stop the server with `Ctrl+C`; use `docker compose down` to remove its container.

## Local Development

```bash
conda activate djangoDev
cp .env.example .env          # first time only
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000/ for the public site, http://127.0.0.1:8000/admin/
for the Django admin, and http://127.0.0.1:8000/panel/ for the branded staff
inventory panel.

