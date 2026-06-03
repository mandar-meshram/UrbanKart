from .models import Registration
from django.shortcuts import redirect


def create_or_update_user(backend, user, response, *args, **kwargs):

    if backend.name == 'google-oauth2':

        email = response.get('email', '')
        first_name = response.get('given_name', '')
        last_name = response.get('family_name', '')

        if not email:
            return

        try:
            # Existing user
            current_user = Registration.objects.get(email=email)

        except Registration.DoesNotExist:
            # Create new OAuth user
            current_user = Registration.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password='',
                confirm_password='',
                is_admin=False,
                auth_provider='google'
            )

        # Store session manually
        backend.strategy.session_set('user_id', current_user.id)
        backend.strategy.session_set('user_name', current_user.first_name)
        backend.strategy.session_set('is_admin', current_user.is_admin)