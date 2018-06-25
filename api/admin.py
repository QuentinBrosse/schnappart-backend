from django.contrib import admin
from .models import Project, ImmoSource, Search, SearchResult
from .models import Feature, SearchResultFeature

admin.site.site_header = 'Schnappart Administration'
admin.site.site_title = admin.site.site_header

admin.site.register(Project)
admin.site.register(ImmoSource)


class SearchAdmin(admin.ModelAdmin):
    fields = ('url', 'project')
    list_display = ('immo_source', 'project', 'url')

admin.site.register(Search, SearchAdmin)


class SearchResultFeatureInline(admin.TabularInline):
    model = SearchResultFeature
    extra = 1


class SearchResultAdmin(admin.ModelAdmin):

    def project(self, obj):
        return obj.search.project

    list_display = ('title', 'project')
    list_filter = ('search__project__name', 'zipcode', 'alive')
    inlines = (SearchResultFeatureInline,)

admin.site.register(SearchResult, SearchResultAdmin)


class FeatureAdmin(admin.ModelAdmin):
    prepopulated_fields = {'key': ('label',), }

admin.site.register(Feature, FeatureAdmin)

admin.site.register(SearchResultFeature)
