import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

BOOK_SERVICE_URL = 'http://book-service:8005'

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=False, methods=['get'], url_path='customer/(?P<customer_id>[^/.]+)')
    def by_customer(self, request, customer_id=None):
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            serializer = self.get_serializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')

        # Check if book exists via book-service
        try:
            resp = requests.get(f'{BOOK_SERVICE_URL}/books/{book_id}/', timeout=5)
            if resp.status_code != 200:
                return Response(
                    {'error': f'Book with id {book_id} not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': f'Could not verify book: {e}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return super().create(request, *args, **kwargs)
