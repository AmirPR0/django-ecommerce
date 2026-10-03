from django.shortcuts import render
from allauth.account.views import PasswordChangeView


class CustomPasswordChangeView(PasswordChangeView):
    """Redirect the user to the home page after changing the password."""

    def get_success_url(self):
        return "/"