from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Products    
from .forms import ProductForm
from Registration.decorators import admin_required
from django.contrib import messages


# Create your views here.
@admin_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('add_product')
    else:
        form = ProductForm()
    
    return render(request, 'add_product.html', {'form': form})  


def view_products(request, pk):
    products = Products.objects.all().filter(category_id=pk)
    return render(request, 'view_product.html', {'products': products})