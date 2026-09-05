from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CarBrandForm, CarImageFormSet, CarListingForm, InquiryForm
from .models import CarBrand, CarListing, Inquiry


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


# ---------------------------------------------------------------------------
# Staff-only administration panel (branded to match the public site design).
# ---------------------------------------------------------------------------

def is_staff_user(user):
    return user.is_active and user.is_staff


class PanelLoginView(auth_views.LoginView):
    template_name = 'panel/login.html'
    redirect_authenticated_user = True


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_dashboard(request):
    context = {
        'total_cars': CarListing.objects.count(),
        'available_cars': CarListing.objects.filter(is_available=True).count(),
        'featured_cars': CarListing.objects.filter(is_featured=True).count(),
        'total_brands': CarBrand.objects.count(),
        'new_inquiries': Inquiry.objects.filter(is_resolved=False).count(),
        'recent_cars': CarListing.objects.order_by('-created_at')[:5],
        'recent_inquiries': Inquiry.objects.order_by('-created_at')[:5],
    }
    return render(request, 'panel/dashboard.html', context)


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_car_list(request):
    cars = CarListing.objects.select_related('brand').order_by('-created_at')
    query = request.GET.get('q')
    if query:
        cars = cars.filter(model_name__icontains=query)

    paginator = Paginator(cars, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'panel/car_list.html', {'page_obj': page_obj, 'query': query or ''})


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_car_create(request):
    if request.method == 'POST':
        form = CarListingForm(request.POST)
        if form.is_valid():
            car = form.save()
            formset = CarImageFormSet(request.POST, request.FILES, instance=car)
            if formset.is_valid():
                formset.save()
                messages.success(request, f'"{car}" was added to the inventory.')
                return redirect('panel:car_list')
        else:
            formset = CarImageFormSet(request.POST, request.FILES)
    else:
        form = CarListingForm()
        formset = CarImageFormSet()

    return render(request, 'panel/car_form.html', {
        'form': form, 'formset': formset, 'is_new': True,
    })


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_car_edit(request, pk):
    car = get_object_or_404(CarListing, pk=pk)

    if request.method == 'POST':
        form = CarListingForm(request.POST, instance=car)
        formset = CarImageFormSet(request.POST, request.FILES, instance=car)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'"{car}" was updated.')
            return redirect('panel:car_list')
    else:
        form = CarListingForm(instance=car)
        formset = CarImageFormSet(instance=car)

    return render(request, 'panel/car_form.html', {
        'form': form, 'formset': formset, 'car': car, 'is_new': False,
    })


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_car_delete(request, pk):
    car = get_object_or_404(CarListing, pk=pk)
    if request.method == 'POST':
        name = str(car)
        car.delete()
        messages.success(request, f'"{name}" was removed from the inventory.')
        return redirect('panel:car_list')
    return render(request, 'panel/car_confirm_delete.html', {'car': car})


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_brand_list(request):
    brands = CarBrand.objects.order_by('name')

    if request.method == 'POST':
        form = CarBrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand added.')
            return redirect('panel:brand_list')
    else:
        form = CarBrandForm()

    return render(request, 'panel/brand_list.html', {'brands': brands, 'form': form})


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_brand_delete(request, pk):
    brand = get_object_or_404(CarBrand, pk=pk)
    if request.method == 'POST':
        if brand.listings.exists():
            messages.error(request, f'Cannot delete "{brand}" while it has car listings.')
        else:
            brand.delete()
            messages.success(request, 'Brand removed.')
    return redirect('panel:brand_list')


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_inquiry_list(request):
    inquiries = Inquiry.objects.select_related('car').order_by('-created_at')
    status = request.GET.get('status')
    if status == 'open':
        inquiries = inquiries.filter(is_resolved=False)
    elif status == 'resolved':
        inquiries = inquiries.filter(is_resolved=True)

    paginator = Paginator(inquiries, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'panel/inquiry_list.html', {'page_obj': page_obj, 'status': status or ''})


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_inquiry_toggle(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    if request.method == 'POST':
        inquiry.is_resolved = not inquiry.is_resolved
        inquiry.save(update_fields=['is_resolved'])
    return redirect('panel:inquiry_list')

