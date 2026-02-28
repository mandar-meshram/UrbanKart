from django.http import HttpResponseForbidden
from functools import wraps
from .models import Registration

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('user_id'):
            from django.shortcuts import redirect
            return redirect('login_user')
        
        try:
            user = Registration.objects.get(id=request.session['user_id'])
            if not user.is_admin:
                return HttpResponseForbidden('Admin access required. You dont have permission to access the page.')
        except Registration.DoesNotExist:
            return HttpResponseForbidden('User not found.')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view