from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecommendationViewSet, recommend_books

router = DefaultRouter()
router.register(r'recommendations', RecommendationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recommend/', recommend_books, name='recommend-books'),
]
