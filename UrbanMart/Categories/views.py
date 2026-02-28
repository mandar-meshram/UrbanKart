from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category
from .forms import CategoryForm
from Registration.decorators import admin_required
from django.contrib import messages

# Create your views here.
@admin_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('add_category')  
    else:
        form = CategoryForm()
    
    return render(request, 'add_category.html', {'form': form})