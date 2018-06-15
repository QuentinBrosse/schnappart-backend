from django.urls import path
from . import views

urlpatterns = [

    # Search Results
    path(
        'search-results/by-project/<int:project_pk>/',
        views.SearchResultListView.as_view()
    ),
    path(
        'search-results/<int:pk>/',
        views.SearchResultUpdateView.as_view()
    )
]
