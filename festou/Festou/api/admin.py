from django.contrib import admin
from .models import User, Place, Transaction, Score
# Register your models here.
#admin.site.register(Place)
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Score)


class CheckedFilter(admin.SimpleListFilter):					#filter for checker
    title = 'Checked'
    parameter_name = 'checked'

    def lookups(self, request, model_admin):
        return (
            ('none', 'None'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'none':
            return queryset.filter(checked__isnull=True)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'location', 'capacity', 'description', 'id_owner', 'checked')
    list_filter = (CheckedFilter,)
