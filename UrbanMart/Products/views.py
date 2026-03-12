from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Products    
from .forms import ProductForm
from Registration.decorators import admin_required
from django.contrib import messages
from Categories.models import Category


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
    category = get_object_or_404(Category, id=pk)
    products = Products.objects.all().filter(category=category)
    return render(request, 'view_product.html', {'products': products, 'category': category})