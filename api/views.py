from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from api.models import Meal, Rating
from api.serializers import MealSerializer, RatingSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class Meal_View(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    
    # sub_url: /api/meal/1/rating/ (GET) for deletion rating of meal with body({meal_id: id})
    @action(detail=True, methods=['DELETE'], url_path='rating')
    def delete_rating(self, request, pk=None):
        print(f"works pk: {pk}")
        meal = get_object_or_404(Meal, id= request.data.get('meal_id'))
        rating = Rating.objects.filter(meal= meal, user= 1)
        if rating.exists():
            rating.delete()
            return Response({"detail": "Rating deleted successfully"}, status= 204)
        else:
            return Response({"detail": "Rating not found"}, status= 404)


        
   
    #   sub_url: /api/meal/1/rate/3 (POST/PATCH) for rating meal with id=1 with 3 stars
    @action(detail=True, methods=['POST','PATCH'], url_path='rate/(?P<stars>[1-5])')
    def set_rating(self, request, pk=None, stars=None):
        try:
            stars = int(stars)
        except:
            return Response({"detail": "Invalid stars"}, status=400)
        
        if stars > 5 or stars < 1:
            return Response({"detail": "You have to rate between [1:5]"}, status=400)
        
        meal = get_object_or_404(Meal, id=pk)
        
        rating = Rating.objects.filter(meal=meal, user=1)
        
        if not rating.exists():
            # if  request.method == 'POST':   # create new rating
            #     serializer = RatingSerializer(data={'meal': meal.id, 'user': 1, 'stars': stars})
            #     if serializer.is_valid():
            #         serializer.save()
            #         return Response(serializer.data, status=201)
            #     else:
            #         return Response(serializer.errors, status=400)
            # else:
            #     return Response({"detail": "request method must be POST"}, status=405)
            if request.method == 'POST':
                newRate = Rating.objects.create(meal=meal, user_id=1, stars=stars)
                # newRate.save() لانحتاج لها لاننا استخدمنا create
                serializer = RatingSerializer(newRate, many=False)
                return Response({"detail": "Rating added successfully","serial":serializer.data}, status=201)
            else:
                return Response(data={"detail": "request method must be POST"}, status=405)
        else:
            if  request.method == 'PATCH':   # update existing rating
                rating = rating.first()
                rating.stars = stars
                rating.save()
                ser = RatingSerializer(rating, many=False)
                return Response({"detail": "Rating updated successfully","ser ":ser.data}, status=200)
            else:
                return Response({"detail": "request method must be PATCH"}, status=405)
            
              
                 
class Rating_View(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer