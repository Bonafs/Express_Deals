from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import HttpResponse

# Temporary placeholder views
class ProductListView(ListView):
    def get(self, request):
        return HttpResponse("Product List View - Coming Soon!")

class ProductDetailView(DetailView):
    def get(self, request, pk):
        return HttpResponse(f"Product Detail View for Product {pk} - Coming Soon!")

class CategoryListView(ListView):
    def get(self, request, slug):
        return HttpResponse(f"Category List View for {slug} - Coming Soon!")
