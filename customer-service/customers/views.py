import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer, CustomerCreateSerializer, UpdateCustomerSerializer

CART_SERVICE_URL = 'http://cart-service:8006'


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerCreateSerializer
        elif self.action in ['update', 'partial_update', 'update_customer']:
            return UpdateCustomerSerializer
        return CustomerSerializer

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

        # Return full data with CustomerSerializer
        out = CustomerSerializer(customer).data
        headers = self.get_success_headers(out)
        return Response(out, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """PUT - full update customer"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        return Response(CustomerSerializer(customer).data)

    def partial_update(self, request, *args, **kwargs):
        """PATCH - partial update customer"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=['put', 'patch'], url_path='update-info')
    def update_customer(self, request, pk=None):
        """
        Cập nhật thông tin customer (full_name, job, address, ...)
        PUT/PATCH /customers/{id}/update-info/
        """
        customer = self.get_object()
        partial = request.method == 'PATCH'
        serializer = UpdateCustomerSerializer(customer, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        return Response({
            'message': 'Customer updated successfully',
            'customer': CustomerSerializer(customer).data
        })

    @action(detail=True, methods=['get'], url_path='cart')
    def get_cart(self, request, pk=None):
        """
        Lấy giỏ hàng của customer
        GET /customers/{id}/cart/
        """
        customer = self.get_object()
        try:
            resp = requests.get(
                f'{CART_SERVICE_URL}/carts/customer/{customer.id}/',
                timeout=5
            )
            if resp.status_code == 200:
                return Response(resp.json())
            return Response(
                {'error': 'Cart not found', 'customer_id': customer.id},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Cannot connect to cart service: {e}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @action(detail=True, methods=['post'], url_path='cart/add-item')
    def add_to_cart(self, request, pk=None):
        """
        Thêm sách vào giỏ hàng của customer
        POST /customers/{id}/cart/add-item/
        Body: { "book_id": 1, "quantity": 2 }
        """
        customer = self.get_object()
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity', 1)

        if not book_id:
            return Response({'error': 'book_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get customer's cart
            cart_resp = requests.get(
                f'{CART_SERVICE_URL}/carts/customer/{customer.id}/',
                timeout=5
            )
            if cart_resp.status_code != 200:
                return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

            cart = cart_resp.json()

            # Add item to cart
            resp = requests.post(
                f'{CART_SERVICE_URL}/cart-items/',
                json={'cart': cart['id'], 'book_id': int(book_id), 'quantity': int(quantity)},
                timeout=5
            )
            return Response(resp.json(), status=resp.status_code)
        except Exception as e:
            return Response(
                {'error': f'Cannot connect to cart service: {e}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @action(detail=True, methods=['put', 'patch'], url_path='cart/update-item/(?P<item_id>[^/.]+)')
    def update_cart_item(self, request, pk=None, item_id=None):
        """
        Cập nhật số lượng sản phẩm trong giỏ hàng
        PUT/PATCH /customers/{id}/cart/update-item/{item_id}/
        Body: { "quantity": 3 }
        """
        customer = self.get_object()
        quantity = request.data.get('quantity')

        if quantity is None:
            return Response({'error': 'quantity is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            resp = requests.patch(
                f'{CART_SERVICE_URL}/cart-items/{item_id}/',
                json={'quantity': int(quantity)},
                timeout=5
            )
            return Response(resp.json(), status=resp.status_code)
        except Exception as e:
            return Response(
                {'error': f'Cannot connect to cart service: {e}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @action(detail=True, methods=['delete'], url_path='cart/remove-item/(?P<item_id>[^/.]+)')
    def remove_cart_item(self, request, pk=None, item_id=None):
        """
        Xóa sản phẩm khỏi giỏ hàng
        DELETE /customers/{id}/cart/remove-item/{item_id}/
        """
        self.get_object()  # verify customer exists
        try:
            resp = requests.delete(
                f'{CART_SERVICE_URL}/cart-items/{item_id}/',
                timeout=5
            )
            if resp.status_code == 204:
                return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)
            return Response(resp.json(), status=resp.status_code)
        except Exception as e:
            return Response(
                {'error': f'Cannot connect to cart service: {e}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
