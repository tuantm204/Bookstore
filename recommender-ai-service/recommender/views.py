import random
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Recommendation
from .serializers import RecommendationSerializer
import requests

BOOK_SERVICE_URL = 'http://book-service:8005'

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

@api_view(['GET'])
def recommend_books(request):
    """Return a random list of recommended books."""
    try:
        resp = requests.get(f'{BOOK_SERVICE_URL}/books/', timeout=5)
        if resp.status_code == 200:
            books = resp.json()
            if isinstance(books, dict) and 'results' in books:
                books = books['results']
            sample_size = min(5, len(books))
            recommended = random.sample(books, sample_size) if books else []
            return Response({'recommended_books': recommended})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response({'recommended_books': []})
