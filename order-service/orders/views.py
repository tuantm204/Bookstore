import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

PAY_SERVICE_URL = 'http://pay-service:8008'
SHIP_SERVICE_URL = 'http://ship-service:8009'
CART_SERVICE_URL = 'http://cart-service:8006'
BOOK_SERVICE_URL = 'http://book-service:8005'

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        customer_id = request.data.get('customer_id')
        address = request.data.get('address', 'Default Address')

        # Get cart items
        try:
            cart_resp = requests.get(
                f'{CART_SERVICE_URL}/carts/customer/{customer_id}/',
                timeout=5
            )
            if cart_resp.status_code != 200:
                return Response({'error': 'Cart not found'}, status=status.HTTP_400_BAD_REQUEST)
            cart_data = cart_resp.json()
        except Exception as e:
            return Response({'error': f'Cannot reach cart service: {e}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        cart_items = cart_data.get('items', [])
        if not cart_items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total and create order
        total = 0
        order_items_data = []
        for item in cart_items:
            try:
                book_resp = requests.get(f'{BOOK_SERVICE_URL}/books/{item["book_id"]}/', timeout=5)
                if book_resp.status_code == 200:
                    book = book_resp.json()
                    price = float(book['price'])
                    total += price * item['quantity']
                    order_items_data.append({
                        'book_id': item['book_id'],
                        'quantity': item['quantity'],
                        'price': price
                    })
            except Exception:
                pass

        order = Order.objects.create(customer_id=customer_id, total_amount=total)
        for oi in order_items_data:
            OrderItem.objects.create(order=order, **oi)

        # Call pay-service
        try:
            requests.post(f'{PAY_SERVICE_URL}/payments/', json={
                'order_id': order.id,
                'amount': str(total),
                'method': 'cash'
            }, timeout=5)
        except Exception as e:
            print(f"Warning: pay-service call failed: {e}")

        # Call ship-service
        try:
            requests.post(f'{SHIP_SERVICE_URL}/shipments/', json={
                'order_id': order.id,
                'address': address
            }, timeout=5)
        except Exception as e:
            print(f"Warning: ship-service call failed: {e}")

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
