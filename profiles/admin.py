from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'is_member',
        'default_town_or_city',
        'default_country'
        )
    list_editable = ('is_member',)


admin.site.register(UserProfile, UserProfileAdmin)
