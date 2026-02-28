from .models import Registration
from django.shortcuts import redirect


def create_or_update_user(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        email = response.get('email','')
        first_name = response.get('given_name', '')
        last_name = response.get('family_name','')

        if email:
            try:
                existing_user = Registration.objects.get(email=email)
                backend.strategy.session['user_id'] = existing_user.id
                backend.strategy.session['user_name'] = existing_user.first_name
                backend.strategy.session['is_admin'] = existing_user.is_admin

            except Registration.DoesNotExist:
                new_user = Registration(
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    password = 'oauth_user',
                    confirm_password = 'oauth_user',
                    is_admin = False
                )
            new_user.save()

            backend.strategy.session['user_id'] = new_user.id
            backend.strategy.session['user_name'] = new_user.first_name
            backend.strategy.session['is_admin'] = new_user.is_admin