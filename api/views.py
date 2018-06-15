from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, UpdateAPIView
from .models import SearchResult, Project
from .serializers import SearchResultSerializer
from .permissions import IsOwner, IsOwnerOfSearchResult


class SearchResultListView(ListAPIView):
    """
    List search results by project.
    """

    serializer_class = SearchResultSerializer
    lookup_url_kwarg = 'project_pk'
    permission_classes = (IsOwner,)

    def get_queryset(self):
        """
        This view should return a list of all SearchResult by
        the project pk passed in the URL.
        """
        project_pk = self.kwargs['project_pk']
        project = Project.objects.get(pk=project_pk)
        self.check_object_permissions(self.request, project)
        return SearchResult.objects \
            .filter(
                search__project=project,
                alive=True,
            ) \
            .order_by('-publication_date') \
            .all()


class SearchResultUpdateView(UpdateAPIView):
    """
    Update a search result.
    """

    queryset = SearchResult.objects.all()
    serializer_class = SearchResultSerializer
    permission_classes = (IsOwnerOfSearchResult,)
