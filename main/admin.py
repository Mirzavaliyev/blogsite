from django.contrib import admin #Admin panelini sozlash va boshqarish modulini olib keladi
from .models import Post, Category #models.py faylidan Post va Category modullarini olib keladi


# Register your models here.
@admin.register(Post) #Post modelini admin panelda ishlatish uchun royhatga oladi
class PastAdmin(admin.ModelAdmin): #Post modelini admin paneldan boshqarish uchun sozlamalar belgilaydi
    list_display = ['title', 'content','created_at', 'views_count']
    list_filter = ['category']
@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name']
