from django.contrib import admin

from .models import Literature

# Register your models here.
@admin.register(Literature)
class LiteratureAdmin(admin.ModelAdmin):
    list_display = ('title', 'journal_abbr', 'doi', 'publication_year',)