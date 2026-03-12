from django.shortcuts import render
from Registration.models import Registration
from Categories.models import Category



def homepage(request):
    user_name = request.session.get('user_name', None)
    user_id = request.session.get('user_id', None)

    # to check if user is admin
    is_admin = False
    if user_id:
        try:
            user = Registration.objects.get(id=user_id)
            is_admin = user.is_admin
        except Registration.DoesNotExist:
            is_admin = False

    # Get the 4 main categories by name (case-insensitive)
    categories = {
        'fashion': Category.objects.filter(name__icontains='Fashion').first(),
        'electronics': Category.objects.filter(name__icontains='Electronics').first(),
        'groceries': Category.objects.filter(name__icontains='Groceries').first(),
        'home': Category.objects.filter(name__icontains='Home').first(),
    }

    return render(request, 'homepage.html', {
        'user_name': user_name,
        'is_admin': is_admin,
        'user_id': user_id,
        'categories': categories
    })  