from rest_framework import serializers
from .models import SearchResult, SearchResultFeature, Feature


class SearchResultFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchResultFeature
        fields = '__all__'


class SearchResultFeatureReadOnlySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    value = serializers.ReadOnlyField()
    search_result = serializers.ReadOnlyField(source='search_result.id')

    class Meta:
        model = SearchResultFeature
        fields = ('id', 'value', 'feature', 'search_result')
        depth = 1


class SearchResultSerializer(serializers.ModelSerializer):
    features = SearchResultFeatureReadOnlySerializer(
        source="searchresultfeature_set",
        many=True
    )

    class Meta:
        model = SearchResult
        fields = '__all__'
        depth = 1


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'
