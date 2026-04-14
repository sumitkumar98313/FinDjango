from django.contrib import admin
from .models import Profile, Transaction


# register Profile model in admin panel
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'monthly_budget', 'has_picture')
    search_fields = ('user__username',)
    list_per_page = 20

    # shows green tick or red cross for whether user has a picture
    def has_picture(self, obj):
        return bool(obj.profile_picture)
    has_picture.boolean = True
    has_picture.short_description = 'Picture'


# register Transaction model in admin panel
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'type', 'amount', 'category', 'date')
    search_fields = ('user__username', 'description')
    # can filter transactions by type, category or date in admin
    list_filter = ('type', 'category', 'date')
    list_per_page = 20
