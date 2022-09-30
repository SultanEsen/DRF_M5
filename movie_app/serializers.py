from rest_framework import serializers
from .models import Director, Movie, Review


class DirectorListSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = 'id name movies_count'.split()

    def get_movies_count(self, obj_director):
        return obj_director.movies.count()


class MoviesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'id title description duration director'.split()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['director'] = instance.director.name

        return response


class ReviewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text movie stars'.split()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['movie'] = instance.movie.title

        return response


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text movie stars'.split()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['movie'] = instance.movie.title

        return response


class MoviesReviewsListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title reviews rating'.split()

    def get_rating(self, obj_movie):
        summa = 0
        for s in obj_movie.reviews.all():
            summa += s.stars
        return round(summa / obj_movie.reviews.count(), 1) if obj_movie.reviews.count() else "No rating"
