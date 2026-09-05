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

Visit http://127.0.0.1:8000/ for the public site, http://127.0.0.1:8000/admin/
for the Django admin, and http://127.0.0.1:8000/panel/ for the branded staff
inventory panel.

