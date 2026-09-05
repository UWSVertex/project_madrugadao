from django.db import models
from django.urls import reverse


class CarBrand(models.Model):
    """A vehicle manufacturer/brand, e.g. Toyota, Honda."""

    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CarListing(models.Model):
    FUEL_GASOLINE = 'gasoline'
    FUEL_DIESEL = 'diesel'
    FUEL_HYBRID = 'hybrid'
    FUEL_ELECTRIC = 'electric'
    FUEL_CHOICES = [
        (FUEL_GASOLINE, 'Gasoline'),
        (FUEL_DIESEL, 'Diesel'),
        (FUEL_HYBRID, 'Hybrid'),
        (FUEL_ELECTRIC, 'Electric'),
    ]

    TRANSMISSION_MANUAL = 'manual'
    TRANSMISSION_AUTOMATIC = 'automatic'
    TRANSMISSION_CHOICES = [
        (TRANSMISSION_MANUAL, 'Manual'),
        (TRANSMISSION_AUTOMATIC, 'Automatic'),
    ]

    BODY_SEDAN = 'sedan'
    BODY_SUV = 'suv'
    BODY_HATCHBACK = 'hatchback'
    BODY_PICKUP = 'pickup'
    BODY_COUPE = 'coupe'
    BODY_VAN = 'van'
    BODY_CHOICES = [
        (BODY_SEDAN, 'Sedan'),
        (BODY_SUV, 'SUV'),
        (BODY_HATCHBACK, 'Hatchback'),
        (BODY_PICKUP, 'Pickup'),
        (BODY_COUPE, 'Coupe'),
        (BODY_VAN, 'Van'),
    ]

    brand = models.ForeignKey(CarBrand, on_delete=models.PROTECT, related_name='listings')
    model_name = models.CharField(max_length=100, verbose_name='Model')
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.PositiveIntegerField(help_text='Mileage in kilometers')
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default=FUEL_GASOLINE)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default=TRANSMISSION_AUTOMATIC)
    body_type = models.CharField(max_length=20, choices=BODY_CHOICES, default=BODY_SEDAN)
    color = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.year} {self.brand} {self.model_name}'

    def get_absolute_url(self):
        return reverse('carlisting:car_detail', args=[self.pk])

    @property
    def primary_image(self):
        image = self.images.filter(is_primary=True).first()
        return image or self.images.first()


class CarImage(models.Model):
    car = models.ForeignKey(CarListing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'uploaded_at']

    def __str__(self):
        return f'Image for {self.car}'


class Inquiry(models.Model):
    car = models.ForeignKey(CarListing, on_delete=models.SET_NULL, related_name='inquiries', blank=True, null=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f'Inquiry from {self.name} ({self.created_at:%Y-%m-%d})'
