from rest_framework import serializers
from .models import SearchResult, SearchResultFeature


class SearchResultFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchResultFeature
        fields = '__all__'


class SearchResultFeatureReadOnlySerializer(serializers.ModelSerializer):
    relation_id = serializers.ReadOnlyField(source='id')
    value = serializers.ReadOnlyField()
    key = serializers.ReadOnlyField(source='feature.key')
    label = serializers.ReadOnlyField(source='feature.label')

    class Meta:
        model = SearchResultFeature
        fields = ('relation_id', 'value', 'key', 'label')


class SearchResultSerializer(serializers.ModelSerializer):
    features = SearchResultFeatureReadOnlySerializer(
        source="searchresultfeature_set",
        many=True
    )

    class Meta:
        model = SearchResult
        fields = '__all__'
        depth = 1
