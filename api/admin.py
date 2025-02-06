from django.contrib import admin
from .models import Meal, Rating
from django.contrib.auth.models import User
from django.db.models import Avg


class MaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'average_rating']
    search_fields = ['title', 'description']
    list_filter = ['title', 'description']
    ordering = ('-title', ) # reversed order by ( - ) symbol
    
    def average_rating(self, obj):
        # Calculate the average rating for the meal
        ratings = obj.ratingsoo.all() # == obj.ratingsoo.filter(meal=obj).values('stars')
        print("ratings: ", ratings.values())
        if ratings.exists():
            return int(ratings.aggregate(Avg('stars'))['stars__avg'])
        return None
    
    average_rating.short_description = 'Average Rating'
    
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'meal', 'user', 'stars']
    list_filter = ['meal', 'user']
    

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0 

class MealInline(admin.TabularInline):
    model = Meal
    extra = 0 
    
class UserAdmin(admin.ModelAdmin):
    list_display = [ 'username', 'email', 'definition']
    inlines = [RatingInline, MealInline]
    
    def definition(self, obj):
        # Show the number of meals the user has created
        uses = obj.useroo.all() # == obj.useroo.filter(user=obj).values('user_id')
        print("uses: ", uses.values())
        if uses.exists():
            return uses.count()
        return None
    
    definition.short_description = 'Meals created'

# إعادة تسجيل UserAdmin
admin.site.unregister(User)  # إلغاء تسجيل UserAdmin الافتراضي
admin.site.register(User, UserAdmin)  # إعادة تسجيله مع التخصيص

admin.site.register(Meal, MaleAdmin)
admin.site.register(Rating, RatingAdmin)