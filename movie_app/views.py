# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DirectorListSerializer, MoviesListSerializer, ReviewsListSerializer
from .serializers import MoviesReviewsListSerializer
from .models import Director, Movie, Review
from rest_framework import status


@api_view(['GET', 'POST'])
def directors_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorListSerializer(directors, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        # print(request.data)
        director = Director.objects.create(
            name=request.data.get('name')
        )
        # print(director)
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Successfully created'}
                        )


@api_view(['GET', 'PUT', 'DELETE'])
def director_item_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data='error: Director not found'
                        )
    if request.method == 'GET':
        return Response(data=DirectorListSerializer(director).data)
    elif request.method == 'DELETE':
        director.delete()
        return Response(
            data={'message': 'Successfully deleted'},
            status=status.HTTP_204_NO_CONTENT
        )
    else:
        director.name = request.data.get('name')
        director.save()
        return Response(data={'message': 'Successfully updated',
                              'product': DirectorListSerializer(director).data
                              }
                        )


@api_view(['GET', 'POST'])
def movies_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MoviesListSerializer(movies, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        movie = Movie.objects.create(
            title=request.data.get('title'),
            description=request.data.get('description'),
            duration=request.data.get('duration'),
            director_id=request.data.get('director')
        )
        movie.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': "Successfully created"}
                        )


@api_view(['GET', 'PUT', 'DELETE'])
def movie_item_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data='error: Movie not found'
        )
    if request.method == "GET":
        return Response(data=MoviesListSerializer(movie).data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(
            data={'message': 'Successfully deleted'},
            status=status.HTTP_204_NO_CONTENT
        )
    else:
        movie.title = request.data.get('title'),
        movie.description = request.data.get('description'),
        # movie.duration = request.data.get('duration'),
        movie.director_id = request.data.get('director')
        movie.save()
        return Response(
            data={'message': 'Successfully updated',
                  'movie': MoviesListSerializer(movie).data}
        )


@api_view(['GET', 'POST'])
def reviews_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewsListSerializer(reviews, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        review = Review.objects.create(
            text=request.data.get('text'),
            movie_id=request.data.get('movie'),
            stars=request.data.get('stars')
        )
        review.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data={'message': 'Successfully created'}
        )


@api_view(['GET', 'PUT', 'DELETE'])
def review_item_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data='error: Review not found')
    if request.method == 'GET':
        return Response(data=ReviewsListSerializer(review).data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(
            data={'message': 'Successfully deleted'},
            status=status.HTTP_204_NO_CONTENT
        )
    else:
        review.text = request.data.get('text')
        review.movie_id = request.data.get('movie')
        review.stars = request.data.get('stars')
        review.save()
        return Response(
            data={'message': 'Successfully updated',
                  'review': ReviewsListSerializer(review).data}
        )


@api_view(['GET'])
def movies_reviews_view(request):
    movies_reviews = Movie.objects.all()
    data = MoviesReviewsListSerializer(movies_reviews, many=True).data
    return Response(data=data)
