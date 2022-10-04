from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class DirectorBaseValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class DirectorCreateSerializer(DirectorBaseValidateSerializer):
    def validate_name(self, name):
        if Director.objects.filter(name=name):
            raise ValidationError('Name of director must be unique')
        return name


class DirectorUpdateSerializer(DirectorBaseValidateSerializer):
    pass


class MovieBaseValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_null=True, allow_blank=True)
    duration = serializers.CharField(allow_blank=True, allow_null=True)
    director = serializers.IntegerField(min_value=1)

    def validate_director(self, director):
        try:
            Director.objects.get(id=director)
        except Director.DoesNotExist:
            raise ValidationError(f'Director (id = {director} does not exist)')
        return director


class MovieCreateSerializer(MovieBaseValidateSerializer):
    def validate_title(self, title):
        if Movie.objects.filter(title=title):
            raise ValidationError('Title must be unique')
        return title


class MovieUpdateSerializer(MovieBaseValidateSerializer):
    pass


class ReviewBaseValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255)
    movie = serializers.IntegerField(min_value=1)
    stars = serializers.IntegerField(default=0, min_value=0, max_value=5)

    def validate_movie(self, movie):
        try:
            Movie.objects.get(id=movie)
        except Movie.DoesNotExist:
            raise ValidationError(f'Movie (id = {movie}) does not exist')
        return movie


class ReviewCreateSerializer(ReviewBaseValidateSerializer):
    pass


class ReviewUpdateSerializer(ReviewBaseValidateSerializer):
    pass

