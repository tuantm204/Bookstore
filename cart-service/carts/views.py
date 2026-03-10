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

    def get_queryset(self):
        queryset = CartItem.objects.all()
        cart_id = self.request.query_params.get('cart')
        if cart_id:
            queryset = queryset.filter(cart_id=cart_id)
        return queryset

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        cart_id = request.data.get('cart')

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

        # Check if item already exists in cart - if so, update quantity
        if cart_id and book_id:
            try:
                existing = CartItem.objects.get(cart_id=cart_id, book_id=book_id)
                new_qty = existing.quantity + int(request.data.get('quantity', 1))
                existing.quantity = new_qty
                existing.save()
                return Response(CartItemSerializer(existing).data, status=status.HTTP_200_OK)
            except CartItem.DoesNotExist:
                pass

        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """PATCH - update quantity"""
        instance = self.get_object()
        quantity = request.data.get('quantity')
        if quantity is not None:
            instance.quantity = int(quantity)
            if instance.quantity <= 0:
                instance.delete()
                return Response({'message': 'Item removed (quantity <= 0)'}, status=status.HTTP_200_OK)
            instance.save()
            return Response(CartItemSerializer(instance).data)
        return super().partial_update(request, *args, **kwargs)
