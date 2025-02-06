from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('meal', views.Meal_View, basename='meal')
router.register('rating', views.Rating_View, basename='rating')

urlpatterns = [
    path('api/', include(router.urls)),
]
