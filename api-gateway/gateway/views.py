import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

SERVICE_MAP = {
    'customers': 'http://customer-service:8001',
    'staffs': 'http://staff-service:8002',
    'managers': 'http://manager-service:8003',
    'catalogs': 'http://catalog-service:8004',
    'books': 'http://book-service:8005',
    'carts': 'http://cart-service:8006',
    'cart-items': 'http://cart-service:8006',
    'orders': 'http://order-service:8007',
    'order-items': 'http://order-service:8007',
    'payments': 'http://pay-service:8008',
    'shipments': 'http://ship-service:8009',
    'comments': 'http://comment-rate-service:8010',
    'recommendations': 'http://recommender-ai-service:8011',
    'recommend': 'http://recommender-ai-service:8011',
}

AUTH_SERVICE_URL = 'http://auth-service:8012'


def index(request):
    return render(request, 'index.html')


def books_page(request):
    return render(request, 'books.html')


def cart_page(request):
    return render(request, 'cart.html')


def customers_page(request):
    return render(request, 'customers.html')


def staffs_page(request):
    return render(request, 'staffs.html')


def managers_page(request):
    return render(request, 'managers.html')


def catalogs_page(request):
    return render(request, 'catalogs.html')


def orders_page(request):
    return render(request, 'orders.html')


def payments_page(request):
    return render(request, 'payments.html')


def shipments_page(request):
    return render(request, 'shipments.html')


def comments_page(request):
    return render(request, 'comments.html')


def recommender_page(request):
    return render(request, 'recommender.html')


def login_page(request):
    return render(request, 'login.html')


def register_page(request):
    return render(request, 'register.html')


def store_page(request):
    return render(request, 'store.html')


def book_detail_page(request):
    return render(request, 'book_detail.html')


def my_cart_page(request):
    return render(request, 'my_cart.html')


def my_orders_page(request):
    return render(request, 'my_orders.html')


def my_profile_page(request):
    return render(request, 'my_profile.html')


def checkout_page(request):
    return render(request, 'checkout.html')


def admin_page(request):
    return render(request, 'admin_dashboard.html')


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def auth_proxy(request, path=''):
    """Proxy requests to auth-service."""
    url = f'{AUTH_SERVICE_URL}/auth/{path}'
    if not url.endswith('/'):
        url += '/'

    headers = {}
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if auth_header:
        headers['Authorization'] = auth_header

    try:
        if request.method == 'GET':
            resp = requests.get(url, params=request.query_params, headers=headers, timeout=10)
        elif request.method == 'POST':
            resp = requests.post(url, json=request.data, headers=headers, timeout=10)
        elif request.method == 'PUT':
            resp = requests.put(url, json=request.data, headers=headers, timeout=10)
        elif request.method == 'PATCH':
            resp = requests.patch(url, json=request.data, headers=headers, timeout=10)
        elif request.method == 'DELETE':
            resp = requests.delete(url, headers=headers, timeout=10)
        else:
            return Response({'error': 'Method not allowed'}, status=405)

        try:
            return Response(resp.json(), status=resp.status_code)
        except ValueError:
            return Response({'detail': resp.text}, status=resp.status_code)

    except requests.exceptions.ConnectionError:
        return Response(
            {'error': 'Cannot connect to auth-service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except requests.exceptions.Timeout:
        return Response(
            {'error': 'Timeout connecting to auth-service'},
            status=status.HTTP_504_GATEWAY_TIMEOUT
        )


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def proxy(request, service, path=''):
    base_url = SERVICE_MAP.get(service)
    if not base_url:
        return Response(
            {'error': f'Unknown service: {service}'},
            status=status.HTTP_404_NOT_FOUND
        )

    url = f'{base_url}/{service}/{path}'
    if not url.endswith('/'):
        url += '/'

    try:
        if request.method == 'GET':
            resp = requests.get(url, params=request.query_params, timeout=10)
        elif request.method == 'POST':
            resp = requests.post(url, json=request.data, timeout=10)
        elif request.method == 'PUT':
            resp = requests.put(url, json=request.data, timeout=10)
        elif request.method == 'PATCH':
            resp = requests.patch(url, json=request.data, timeout=10)
        elif request.method == 'DELETE':
            resp = requests.delete(url, timeout=10)
        else:
            return Response({'error': 'Method not allowed'}, status=405)

        try:
            return Response(resp.json(), status=resp.status_code)
        except ValueError:
            return Response({'detail': resp.text}, status=resp.status_code)

    except requests.exceptions.ConnectionError:
        return Response(
            {'error': f'Cannot connect to {service}'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except requests.exceptions.Timeout:
        return Response(
            {'error': f'Timeout connecting to {service}'},
            status=status.HTTP_504_GATEWAY_TIMEOUT
        )
