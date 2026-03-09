import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer

CART_SERVICE_URL = 'http://cart-service:8006'

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()

        # Auto-create cart for customer
        try:
            requests.post(
                f'{CART_SERVICE_URL}/carts/',
                json={'customer_id': customer.id},
                timeout=5
            )
        except Exception as e:
            print(f"Warning: Could not create cart for customer {customer.id}: {e}")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
