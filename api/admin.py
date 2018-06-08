from django.contrib import admin
from .models import Project, ImmoSource, Search

admin.site.register(Project)
admin.site.register(ImmoSource)


class SearchAdmin(admin.ModelAdmin):
    fields = ('url',)
    list_display = ('immo_source', 'url')

admin.site.register(Search, SearchAdmin)
