from rest_framework import serializers
from .models import SearchResult


class SearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchResult
        fields = '__all__'
        depth = 1
