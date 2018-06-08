from django.contrib import admin
from .models import Project, ImmoSource, Search, SearchResult

admin.site.site_header = 'Schnappart Administration'
admin.site.site_title = admin.site.site_header

admin.site.register(Project)
admin.site.register(ImmoSource)


class SearchAdmin(admin.ModelAdmin):
    fields = ('url',)
    list_display = ('immo_source', 'url')

admin.site.register(Search, SearchAdmin)

admin.site.register(SearchResult)
