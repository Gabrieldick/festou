from django.contrib import admin
from .models import User, Place, Transaction, Score

# Register your models here.

admin.site.register(Transaction)
admin.site.register(Score)

class CheckedFilter(admin.SimpleListFilter):					#filter for checker
    title = 'Checked'
    parameter_name = 'checked'

    def lookups(self, request, model_admin):
        return (
            ('pending', 'pending'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'pending':
            return queryset.filter(checked=0)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'checked')
    list_filter = (CheckedFilter,)

class ReportedFilter(admin.SimpleListFilter):
    title = 'Reported'
    parameter_name = 'reported'

    def lookups(self, request, model_admin):
        return (
            ('reported', 'Reported'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'reported':
            return queryset.filter(reported=True)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name','reported', 'blocked')  # Changed 'name' to 'username'
    list_filter = (ReportedFilter,)
