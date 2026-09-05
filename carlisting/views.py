from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import InquiryForm
from .models import CarBrand, CarListing


def home(request):
    featured_cars = CarListing.objects.filter(is_available=True, is_featured=True)[:6]
    if not featured_cars:
        featured_cars = CarListing.objects.filter(is_available=True)[:6]
    return render(request, 'carlisting/home.html', {'featured_cars': featured_cars})


def car_list(request):
    cars = CarListing.objects.filter(is_available=True)

    brand_id = request.GET.get('brand')
    body_type = request.GET.get('body_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    query = request.GET.get('q')

    if brand_id:
        cars = cars.filter(brand_id=brand_id)
    if body_type:
        cars = cars.filter(body_type=body_type)
    if min_price:
        cars = cars.filter(price__gte=min_price)
    if max_price:
        cars = cars.filter(price__lte=max_price)
    if query:
        cars = cars.filter(model_name__icontains=query)

    paginator = Paginator(cars, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'brands': CarBrand.objects.all(),
        'body_types': CarListing.BODY_CHOICES,
        'request_get': request.GET,
    }
    return render(request, 'carlisting/car_list.html', context)


def car_detail(request, pk):
    car = get_object_or_404(CarListing, pk=pk)

    if request.method == 'POST':
        form = InquiryForm(request.POST, initial={'car': car})
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.car = car
            inquiry.save()
            messages.success(request, 'Thanks! Your inquiry has been sent. We will contact you soon.')
            return redirect('carlisting:car_detail', pk=car.pk)
    else:
        form = InquiryForm(initial={'car': car})

    return render(request, 'carlisting/car_detail.html', {'car': car, 'form': form})


def contact(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks! Your message has been sent. We will contact you soon.')
            return redirect('carlisting:contact')
    else:
        form = InquiryForm()

    return render(request, 'carlisting/contact.html', {'form': form})

