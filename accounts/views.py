from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

# Temporary placeholder views
class RegisterView(View):
    def get(self, request):
        return HttpResponse("Register View - Coming Soon!")

class LoginView(View):
    def get(self, request):
        return HttpResponse("Login View - Coming Soon!")

class LogoutView(View):
    def get(self, request):
        return HttpResponse("Logout View - Coming Soon!")

class ProfileView(View):
    def get(self, request):
        return HttpResponse("Profile View - Coming Soon!")
