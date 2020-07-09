from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Image, Product, Category, Favourites, Opinion
from django.contrib.auth.admin import UserAdmin


class PropertyImageInline(admin.TabularInline):
    model = Image
    extra = 1


class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline, ]
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, PropertyAdmin)


class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name_plural = 'Profile'


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline, ]


admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Favourites)
admin.site.register(Opinion)

