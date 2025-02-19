from rest_framework import serializers
from .models import Meal, Rating
from django.contrib.auth.models import User
from django.db.models import Avg

class MealSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    raters_count = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = ('id', 'title', 'description', 'user', 'author', 'rate', 'raters_count')
        
    #1   get author of meal
    def get_author(self, obj):
        user = User.objects.get(id=obj.user_id)
        return user.username if user else "Unknown"
    
    #2   get Avg of rates of this meal
    def get_rate(self, obj):
        rate = obj.ratingsoo.aggregate(Avg('stars'))['stars__avg']
        if rate is None:
            return 0
        return int(rate)
    
    #3   get number of raters of this meal
    def get_raters_count(self, obj):
        return obj.ratingsoo.count()


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'meal', 'user', 'stars')