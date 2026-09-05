from django.contrib import admin
from django.utils.html import format_html

from .models import CarBrand, CarImage, CarListing, Inquiry

admin.site.site_header = 'Car Sales Admin'
admin.site.site_title = 'Car Sales Admin'
admin.site.index_title = 'Dealership Management'


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    fields = ('image', 'is_primary', 'thumbnail')
    readonly_fields = ('thumbnail',)

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;" />', obj.image.url)
        return '(no image)'
    thumbnail.short_description = 'Preview'


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview')
    search_fields = ('name',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:30px;" />', obj.logo.url)
        return '—'
    logo_preview.short_description = 'Logo'


@admin.register(CarListing)
class CarListingAdmin(admin.ModelAdmin):
    list_display = (
        'thumbnail', 'brand', 'model_name', 'year', 'price', 'mileage',
        'body_type', 'is_available', 'is_featured', 'created_at',
    )
    list_filter = ('brand', 'body_type', 'fuel_type', 'transmission', 'is_available', 'is_featured', 'year')
    search_fields = ('model_name', 'brand__name', 'description')
    list_editable = ('is_available', 'is_featured')
    inlines = [CarImageInline]
    fieldsets = (
        ('Vehicle Info', {
            'fields': ('brand', 'model_name', 'year', 'color', 'body_type')
        }),
        ('Specs', {
            'fields': ('price', 'mileage', 'fuel_type', 'transmission')
        }),
        ('Listing Status', {
            'fields': ('is_available', 'is_featured', 'description')
        }),
    )

    def thumbnail(self, obj):
        image = obj.primary_image
        if image:
            return format_html('<img src="{}" style="height:50px;" />', image.image.url)
        return '(no image)'
    thumbnail.short_description = 'Photo'


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'car', 'created_at', 'is_resolved')
    list_filter = ('is_resolved', 'created_at')
    list_editable = ('is_resolved',)
    search_fields = ('name', 'phone', 'email', 'message')
