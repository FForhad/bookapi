from django.contrib import admin
from .models import CustomUser, Oem, Dealer, Book
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_staff', 'is_active')
    search_fields = ('email',)

@admin.register(Oem)
class OemAdmin(admin.ModelAdmin):
    list_display = ('oem_name', 'oem_number')
    search_fields = ('oem_name',)

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('dealer_name', 'dealer_number', 'oem')
    search_fields = ('dealer_name',)
    list_filter = ('oem',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description')
    search_fields = ('title', 'author')
