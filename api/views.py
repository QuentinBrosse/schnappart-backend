from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView
from django.forms.models import model_to_dict
from .models import SearchResult, Project, SearchResultFeature
from . import serializers
from . import permissions


class CustomAuthToken(ObtainAuthToken):
    """
    Custom obtain auth token view.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        user_dict = model_to_dict(user)
        user_dict['authToken'] = token.key
        user_dict['projects'] = Project.objects \
            .filter(user=user) \
            .values_list('id', flat=True)
        return Response(user_dict)


class SearchResultListView(ListAPIView):
    """
    List accepted search results by project.
    """

    serializer_class = serializers.SearchResultSerializer
    lookup_url_kwarg = 'project_pk'
    permission_classes = (permissions.IsOwner,)

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
                accepted=True,
                alive=True,
            ) \
            .order_by('-publication_date') \
            .all()


class SearchResultPendingListView(ListAPIView):
    """
    List pending search results by project. (where accepted=None)
    """

    serializer_class = serializers.SearchResultSerializer
    lookup_url_kwarg = 'project_pk'
    permission_classes = (permissions.IsOwner,)

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
                accepted=None,
                alive=True,
            ) \
            .order_by('-publication_date') \
            .all()


class SearchResultAcceptView(UpdateAPIView):
    """
    Accept a search result.
    """

    queryset = SearchResult.objects.all()
    serializer_class = serializers.SearchResultSerializer
    permission_classes = (permissions.IsOwnerOfSearchResult,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data={'accepted': True},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class SearchResultRefuseView(UpdateAPIView):
    """
    Refuse a search result.
    """

    queryset = SearchResult.objects.all()
    serializer_class = serializers.SearchResultSerializer
    permission_classes = (permissions.IsOwnerOfSearchResult,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data={'accepted': False},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class SearchResultUpdateView(UpdateAPIView):
    """
    Update a search result.
    """

    queryset = SearchResult.objects.all()
    serializer_class = serializers.SearchResultSerializer
    permission_classes = (permissions.IsOwnerOfSearchResult,)


class SearchResultFeatureCreateView(CreateAPIView):
    """
    Creatre a search result feature.
    """

    queryset = SearchResultFeature.objects.all()
    serializer_class = serializers.SearchResultFeatureSerializer
    permission_classes = (permissions.IsOwnerOfSearchResultM2M,)
